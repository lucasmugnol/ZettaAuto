# AutoMedia AI — Spike Técnico Local (Sprint 1)

O **AutoMedia AI** é uma esteira autônoma de mídia veicular (*Autonomous Media Pipeline*) construída para transformar lote de fotos de veículos em peças publicitárias com Identidade Comercial, cobrindo placas e gerando descrições e títulos comerciais sem intervenção manual.

---

## 🚀 Como Executar o Spike Local

### Requisitos

- Python 3.12+ (ou gerenciador `uv`)

### Instalação

```bash
# 1. Criar ambiente virtual
uv venv .venv --python 3.12

# 2. Instalar dependências
uv pip install --python .venv Pillow pytest psutil
```

### Executar Testes Automatizados

```bash
.venv/Scripts/python.exe -m pytest -v
```

### Executar a Esteira Local (CLI)

```bash
.venv/Scripts/python.exe -m automedia.cli run \
  --input ./input \
  --output ./output \
  --brand ./config/brand.json \
  --vehicle ./config/vehicle.json \
  --pipeline ./config/pipeline.json
```

---

## 📁 Estrutura de Artefatos Gerados

A cada execução, uma pasta única por Job é criada em `./output/<job_id>/`:

```text
output/<job_id>/
├── cover.jpg                   # Capa principal diagramada
├── photos/                     # Galeria com marca d'água e placa coberta
│   ├── photo_01.jpg
│   └── photo_02.jpg
├── title.txt                   # Título comercial do anúncio
├── description.txt             # Descrição comercial detalhada
├── manifest.json               # Manifesto técnico do job
├── benchmark.json              # Métrica e telemetria de execução
└── vehicle_media_package.zip   # Pacote compactado com todos os artefatos
```

---

## 📚 Documentação do Projeto

Toda a documentação técnica e de produto governante (Documentos `000` a `007`) encontra-se na pasta [`docs/`](docs/README.md).
