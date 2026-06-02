# Capstone Bridge

Bridge automatizado entre o Google Sheets público do Capstone Macro FIC FIM e o `fundos_extract.py`
que roda numa rede com firewall (WatchGuard) que bloqueia `docs.google.com`.

## Como funciona

1. GitHub Actions roda `fetch_capstone.py` 3x por dia (8h, 13h, 18h BRT)
2. O script lê o CSV publicado do Sheets (fora da firma → sem firewall)
3. Salva data + cota em `data/capstone.json`
4. Commita o JSON no repo
5. `fundos_extract.py` lê de `https://raw.githubusercontent.com/<USUARIO>/<REPO>/main/data/capstone.json`

## Rodar manualmente

Aba **Actions** → workflow "Fetch Capstone" → "Run workflow".
