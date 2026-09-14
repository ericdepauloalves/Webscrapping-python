"""
main.py
Executa o fluxo completo: coleta identidades, salva em CSV e envia por email.

Uso:
    python src/main.py --quantidade 10
    python src/main.py --quantidade 5 --sem-email   # só gera o CSV, não envia
"""

import argparse
from datetime import datetime

from dotenv import load_dotenv

from scraper import collect_identities, save_to_csv
from mailer import send_csv_by_email


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Web scraper do fakenamegenerator.com")
    parser.add_argument(
        "--quantidade", type=int, default=10, help="Quantidade de identidades a coletar"
    )
    parser.add_argument(
        "--sem-email", action="store_true", help="Não enviar o CSV por email, só gerar o arquivo"
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()

    print(f"Coletando {args.quantidade} identidade(s)...")
    identities = collect_identities(args.quantidade)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"output/identidades_{timestamp}.csv"
    saved_path = save_to_csv(identities, output_path)
    print(f"CSV salvo em: {saved_path}")

    if args.sem_email:
        print("Flag --sem-email usada, pulando envio de email.")
        return

    send_csv_by_email(
        csv_path=str(saved_path),
        subject="Identidades coletadas - Web Scraping",
        body=f"Segue em anexo o CSV com {len(identities)} identidade(s) coletada(s).",
    )


if __name__ == "__main__":
    main()
