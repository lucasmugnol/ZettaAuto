"""CLI Entrypoint for AutoMedia AI Local Spike."""

import sys
import argparse
import logging
from automedia.pipeline import LocalPipeline


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        prog="python -m automedia.cli",
        description="AutoMedia AI — Spike Técnico Local (CLI)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Executar esteira autônoma de mídia local")
    run_parser.add_argument("--input", "-i", required=True, help="Diretório de entrada contendo fotos brutas")
    run_parser.add_argument("--output", "-o", required=True, help="Diretório base de saída")
    run_parser.add_argument("--brand", "-b", required=True, help="Arquivo JSON de configuração da marca")
    run_parser.add_argument("--vehicle", "-v", required=True, help="Arquivo JSON de metadados do veículo")
    run_parser.add_argument("--pipeline", "-p", required=True, help="Arquivo JSON de parâmetros do pipeline")

    args = parser.parse_args()

    if args.command == "run":
        print("=========================================================")
        print(" AUTOMEDIA AI - SPIKE TECNICO LOCAL (SPRINT 1)")
        print("=========================================================")

        pipeline = LocalPipeline()
        job, result = pipeline.run(
            input_dir=args.input,
            output_dir=args.output,
            brand_config_path=args.brand,
            vehicle_config_path=args.vehicle,
            pipeline_config_path=args.pipeline
        )

        print(f"\n[JOB STATUS] : {job.status}")
        print(f"[JOB ID]     : {job.job_id}")
        print(f"[INPUT DIR]  : {job.input_path}")
        print(f"[OUTPUT DIR] : {job.output_path}/{job.job_id}")
        print(f"[IMAGENS]    : {job.successful_images}/{job.total_images} processadas com sucesso")

        if result.success:
            print("\n---------------------------------------------------------")
            print(" ARTEFATOS GERADOS COM SUCESSO:")
            print(f"  [+] Capa Principal      : {result.cover_file}")
            print(f"  [+] Galeria Secundaria  : {len(result.gallery_files)} foto(s)")
            print(f"  [+] Titulo Comercial    : {result.text_title_file}")
            print(f"  [+] Descricao Comercial : {result.text_desc_file}")
            print(f"  [+] Manifesto do Job    : {result.manifest_file}")
            print(f"  [+] Relatorio Benchmark : {result.benchmark_file}")
            print("---------------------------------------------------------")

            if job.warnings:
                print("\n[ALERTAS / WARNINGS]:")
                for w in job.warnings:
                    print(f"  [!] {w}")

            print("\n[OK] Execucao concluida com sucesso (Exit Code: 0).\n")
            sys.exit(0)
        else:
            print("\n---------------------------------------------------------")
            print(" [X] ERRO BLOQUEANTE NA EXECUCAO DO PIPELINE:")
            for err in result.errors:
                print(f"  [-] {err}")
            print("---------------------------------------------------------\n")
            sys.exit(1)


if __name__ == "__main__":
    main()
