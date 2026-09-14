# Web Scraper - Fake Name Generator → CSV → Email

Projeto de portfólio que faz web scraping do [fakenamegenerator.com](https://www.fakenamegenerator.com),
coleta **nome, email e telefone** gerados, salva os dados em um arquivo CSV e envia esse
arquivo por email. A execução é **manual** — você roda o script quando quiser.

## Como funciona

1. `src/scraper.py` faz o request à página do gerador e extrai os campos com BeautifulSoup.
2. `src/main.py` orquestra a coleta de N identidades e salva tudo em `output/identidades_<data>.csv`.
3. `src/mailer.py` envia esse CSV como anexo por email via SMTP.

## Como rodar localmente

### 1. Clonar o repositório e instalar dependências

```bash
git clone https://github.com/SEU_USUARIO/webscraper-fakename.git
cd webscraper-fakename
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar as credenciais de email

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

Edite o `.env` com seu servidor SMTP. Para Gmail:
- `SMTP_HOST=smtp.gmail.com`
- `SMTP_PORT=587`
- `SMTP_PASSWORD` deve ser uma **senha de app** (não a senha normal da sua conta Google).
  Gere uma em: https://myaccount.google.com/apppasswords

> ⚠️ O arquivo `.env` nunca deve ser enviado ao GitHub — ele já está no `.gitignore`.

### 3. Executar

```bash
# Coleta 10 identidades, salva o CSV e envia por email
python src/main.py --quantidade 10

# Só gera o CSV, sem enviar email
python src/main.py --quantidade 10 --sem-email
```

## Estrutura do projeto

```
webscraper-fakename/
├── src/
│   ├── scraper.py   # coleta os dados do site
│   ├── mailer.py    # envia o CSV por email
│   └── main.py       # script principal
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Como subir este projeto no GitHub

```bash
cd webscraper-fakename
git init
git add .
git commit -m "Primeiro commit: web scraper com envio de CSV por email"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/webscraper-fakename.git
git push -u origin main
```

Troque `SEU_USUARIO` pelo seu usuário do GitHub. Se o repositório ainda não existir,
crie um novo repositório vazio em https://github.com/new antes do `git push`.

## Aviso

Os dados coletados são **fictícios**, gerados propositalmente pelo próprio site
para fins de teste — nenhum dado real de pessoas é coletado.
