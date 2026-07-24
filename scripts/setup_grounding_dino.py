import os
import sys
import time
import json
import psutil
from pathlib import Path

def get_ram_usage_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def setup_grounding_dino():
    print("=" * 60)
    print("AutoMedia AI — Setup Grounding DINO (Transformers)")
    print("=" * 60)

    # 1. Confirm running inside .venv
    venv_path = os.environ.get("VIRTUAL_ENV", "")
    python_exe = sys.executable
    print(f"[1/7] Ambiente Python: {python_exe}")
    print(f"      Virtual Env: {venv_path if venv_path else 'Não detectado via VIRTUAL_ENV, prosseguindo com intérprete atual'}")

    # 2. Check PyTorch and Transformers
    try:
        import torch
        import transformers
        import safetensors
        from PIL import Image
        print(f"[2/7] PyTorch: {torch.__version__} (CUDA: {torch.cuda.is_available()})")
        print(f"      Transformers: {transformers.__version__}")
        print(f"      Safetensors: {safetensors.__version__}")
    except ImportError as e:
        print(f"[ERRO] Dependência ausente: {e}")
        sys.exit(1)

    # 3. Target local path
    model_id = "IDEA-Research/grounding-dino-tiny"
    local_dir = Path("models/grounding_dino/grounding-dino-tiny")
    local_dir.mkdir(parents=True, exist_ok=True)
    print(f"[3/7] Diretório do Modelo: {local_dir.resolve()}")

    # 4. Download or verify snapshot
    print(f"[4/7] Verificando / Baixando snapshot oficial de '{model_id}'...")
    from huggingface_hub import snapshot_download

    t0_download = time.time()
    try:
        downloaded_path = snapshot_download(
            repo_id=model_id,
            local_dir=str(local_dir),
            local_dir_use_symlinks=False,
            ignore_patterns=["*.msgpack", "*.h5", "*.ot", "*.ckpt"]
        )
        download_time = time.time() - t0_download
        print(f"      Download / Verificação concluída em {download_time:.2f}s")
    except Exception as e:
        print(f"[ERRO] Falha ao baixar snapshot do HuggingFace: {e}")
        sys.exit(1)

    # Calculate size and files
    total_bytes = 0
    files_list = []
    for f in local_dir.rglob("*"):
        if f.is_file():
            size = f.stat().st_size
            total_bytes += size
            files_list.append((f.name, size))

    total_mb = total_bytes / (1024 * 1024)
    print(f"      Tamanho total local do snapshot: {total_mb:.2f} MB ({total_bytes / (1024**3):.2f} GB)")
    print("      Arquivos principais encontrados:")
    for fname, fsize in files_list:
        print(f"        - {fname}: {fsize / (1024*1024):.2f} MB")

    # Save README metadata in models/grounding_dino
    readme_path = Path("models/grounding_dino/README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"""# Grounding DINO Model — Local Snapshot

- **Modelo Oficial**: `{model_id}`
- **Origem**: [IDEA-Research/grounding-dino-tiny no Hugging Face](https://huggingface.co/IDEA-Research/grounding-dino-tiny)
- **Licença Declarada**: Apache License 2.0 (Permissiva para uso comercial)
- **Tamanho Total Local**: {total_mb:.2f} MB
- **Data de Setup**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **Intérprete**: `{python_exe}`

### Arquivos Esperados
- `model.safetensors` (~689 MB)
- `config.json`
- `preprocessor_config.json`
- `tokenizer_config.json` / `vocab.txt` / `tokenizer.json`

### Execução Offline
O pipeline carrega este modelo exclusivamente via:
```python
AutoProcessor.from_pretrained("{local_dir}", local_files_only=True)
AutoModelForZeroShotObjectDetection.from_pretrained("{local_dir}", local_files_only=True)
```
""")
    print(f"      README documentado em '{readme_path}'")

    # 5. Offline load test & RAM metrics
    ram_before = get_ram_usage_mb()
    print(f"[5/7] Testando carregamento OFFLINE (local_files_only=True)...")
    print(f"      RAM antes do carregamento: {ram_before:.2f} MB")

    from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection

    t0_load = time.time()
    try:
        processor = AutoProcessor.from_pretrained(str(local_dir), local_files_only=True)
        model = AutoModelForZeroShotObjectDetection.from_pretrained(str(local_dir), local_files_only=True)
        model.to("cpu")
        model.eval()
    except Exception as e:
        print(f"[ERRO] Falha ao carregar modelo offline: {e}")
        sys.exit(1)

    load_time_ms = (time.time() - t0_load) * 1000
    ram_after = get_ram_usage_mb()
    print(f"      Modelo carregado com SUCESSO offline!")
    print(f"      Tempo de carregamento (frio): {load_time_ms:.2f} ms")
    print(f"      RAM após o carregamento: {ram_after:.2f} MB (Delta: {ram_after - ram_before:.2f} MB)")

    # 6. Test Zero-shot inference on sample image
    print(f"[6/7] Testando inferência real em 1 imagem...")
    sample_img_path = Path("input/sample_car1.jpg")
    if not sample_img_path.exists():
        # Fallback to any image in input or create dummy RGB image
        input_files = list(Path("input").glob("*.jpg")) + list(Path("validation_real").rglob("*.jpg"))
        if input_files:
            sample_img_path = input_files[0]

    if sample_img_path.exists():
        print(f"      Imagem de teste: '{sample_img_path}'")
        image = Image.open(sample_img_path).convert("RGB")
    else:
        print("      Nenhuma imagem encontrada em input/, criando imagem RGB sintética de teste...")
        image = Image.new("RGB", (800, 600), color=(128, 128, 128))

    prompts = ["car", "pickup truck", "sport utility vehicle", "van"]
    text_prompt = ". ".join(prompts) + "."
    print(f"      Prompt formatado: '{text_prompt}'")

    ram_infer_start = get_ram_usage_mb()

    # First inference (cold)
    t0_inf1 = time.time()
    inputs = processor(images=image, text=text_prompt, return_tensors="pt").to("cpu")
    with torch.no_grad():
        outputs = model(**inputs)

    results = processor.post_process_grounded_object_detection(
        outputs,
        inputs.input_ids,
        threshold=0.30,
        text_threshold=0.25,
        target_sizes=[image.size[::-1]] # (height, width)
    )
    inf1_ms = (time.time() - t0_inf1) * 1000

    # Second inference (warm)
    t0_inf2 = time.time()
    inputs2 = processor(images=image, text=text_prompt, return_tensors="pt").to("cpu")
    with torch.no_grad():
        outputs2 = model(**inputs2)
    results2 = processor.post_process_grounded_object_detection(
        outputs2,
        inputs2.input_ids,
        threshold=0.30,
        text_threshold=0.25,
        target_sizes=[image.size[::-1]]
    )
    inf2_ms = (time.time() - t0_inf2) * 1000
    ram_infer_peak = get_ram_usage_mb()

    detected_boxes = len(results[0]["boxes"]) if results else 0
    print(f"      Primeira inferência (fria): {inf1_ms:.2f} ms")
    print(f"      Segunda inferência (quente): {inf2_ms:.2f} ms")
    print(f"      Pico de RAM na inferência: {ram_infer_peak:.2f} MB")
    print(f"      Caixas detectadas: {detected_boxes}")

    if results and detected_boxes > 0:
        for idx, (box, score, label) in enumerate(zip(results[0]["boxes"], results[0]["scores"], results[0]["labels"])):
            b = [round(x, 1) for x in box.tolist()]
            print(f"        [{idx+1}] Label: '{label}' | Confidence: {score:.3f} | BBox: {b}")

    print("-" * 60)
    print("[SUCESSO] Setup e validação do Grounding DINO concluídos com exito!")
    print(f"          Status do repositório local: OK ({total_mb:.2f} MB)")
    print("=" * 60)

if __name__ == "__main__":
    setup_grounding_dino()
