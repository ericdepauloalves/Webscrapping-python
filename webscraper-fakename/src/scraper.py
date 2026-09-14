"""
scraper.py
Coleta nome, email e telefone gerados pelo fakenamegenerator.com
e salva os resultados em um arquivo CSV.
"""

import csv
import time
import random
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.fakenamegenerator.com/gen-random-us-us.php"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def fetch_identity() -> dict:
    """Faz uma requisição ao site e extrai nome, email e telefone."""
    response = requests.get(BASE_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Nome: está no <h3> dentro do bloco de identidade
    name_tag = soup.select_one("div#identity-name h3, h3")
    name = name_tag.get_text(strip=True) if name_tag else None

    # Email e telefone: aparecem como <dt>Rótulo</dt><dd>Valor</dd>
    email = None
    phone = None
    for dt in soup.find_all("dt"):
        label = dt.get_text(strip=True).lower()
        dd = dt.find_next_sibling("dd")
        if not dd:
            continue
        value = dd.get_text(strip=True)
        if "email" in label:
            email = value
        elif label == "phone":
            phone = value

    return {"nome": name, "email": email, "telefone": phone}


def collect_identities(quantity: int, delay_seconds: float = 1.5) -> list[dict]:
    """Coleta várias identidades, com uma pequena pausa entre requisições."""
    identities = []
    for i in range(quantity):
        identity = fetch_identity()
        identities.append(identity)
        print(f"[{i + 1}/{quantity}] coletado: {identity}")
        if i < quantity - 1:
            time.sleep(delay_seconds + random.uniform(0, 0.5))
    return identities


def save_to_csv(identities: list[dict], output_path: str) -> Path:
    """Salva a lista de identidades em um arquivo CSV."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "email", "telefone"])
        writer.writeheader()
        writer.writerows(identities)

    return path
