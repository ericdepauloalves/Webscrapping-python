"""
ScraperLibrary.py
Library do Robot Framework que expõe como "keywords" as funções
de scraping, geração de CSV e envio de email já criadas em src/.
"""

import sys
from pathlib import Path

# Garante que o pacote src/ seja importável
SRC_PATH = str(Path(__file__).resolve().parent.parent / "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from robot.api.deco import keyword, library  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

from scraper import collect_identities, save_to_csv  # noqa: E402
from mailer import send_csv_by_email  # noqa: E402


@library(scope="GLOBAL")
class ScraperLibrary:
    """Keywords customizados para o robô de web scraping + email."""

    def __init__(self):
        load_dotenv()
        self._identities: list[dict] = []
        self._csv_path: str = ""

    @keyword("Coletar Identidades")
    def coletar_identidades(self, quantidade: int):
        """Faz o scraping de `quantidade` identidades no fakenamegenerator.com."""
        quantidade = int(quantidade)
        self._identities = collect_identities(quantidade)
        return self._identities

    @keyword("Salvar Identidades Em Csv")
    def salvar_identidades_em_csv(self, caminho_saida: str):
        """Salva as identidades já coletadas em um arquivo CSV."""
        if not self._identities:
            raise ValueError("Nenhuma identidade foi coletada ainda. Rode 'Coletar Identidades' antes.")
        saved_path = save_to_csv(self._identities, caminho_saida)
        self._csv_path = str(saved_path)
        return self._csv_path

    @keyword("Enviar Csv Por Email")
    def enviar_csv_por_email(self, assunto: str = "Identidades coletadas - Web Scraping"):
        """Envia o CSV gerado anteriormente como anexo de email."""
        if not self._csv_path:
            raise ValueError("Nenhum CSV foi salvo ainda. Rode 'Salvar Identidades Em Csv' antes.")
        corpo = f"Segue em anexo o CSV com {len(self._identities)} identidade(s) coletada(s)."
        send_csv_by_email(csv_path=self._csv_path, subject=assunto, body=corpo)
