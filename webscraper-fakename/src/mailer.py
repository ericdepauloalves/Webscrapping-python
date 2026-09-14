"""
mailer.py
Envia um arquivo CSV como anexo por email usando SMTP.
Funciona com Gmail (usando senha de app) ou qualquer outro provedor SMTP.
"""

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


def send_csv_by_email(
    csv_path: str,
    subject: str = "Resultado do Web Scraping",
    body: str = "Segue em anexo o CSV com os dados coletados.",
) -> None:
    """Envia o CSV indicado como anexo, usando variáveis de ambiente para as credenciais."""

    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ["SMTP_USER"]
    smtp_password = os.environ["SMTP_PASSWORD"]
    email_from = os.environ.get("EMAIL_FROM", smtp_user)
    email_to = os.environ["EMAIL_TO"]

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_from
    msg["To"] = email_to
    msg.set_content(body)

    csv_file = Path(csv_path)
    with csv_file.open("rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="text",
            subtype="csv",
            filename=csv_file.name,
        )

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

    print(f"Email enviado para {email_to} com o anexo {csv_file.name}")
