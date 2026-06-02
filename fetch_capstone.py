"""
Lê o Google Sheets do Capstone (publicado na web) e salva data + cota em data/capstone.json.

Rodado pelo GitHub Actions 3x por dia (workflow em .github/workflows/fetch.yml).
O fundos_extract.py no PC da firma lê esse JSON via raw.githubusercontent.com.
"""
import csv
import json
import os
import sys
from io import StringIO

import requests

URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRV4vde5JbdVZzDUc2AG0kfTAdupDrrp6exEpHvyclyDwZclEzplU5NGRkjGVR_iq1s3Ei7DE6Yy4tc/"
    "pub?gid=0&single=true&output=csv"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept": "text/csv,*/*;q=0.9",
}


def main():
    r = requests.get(URL, timeout=30, headers=HEADERS, allow_redirects=True)
    r.raise_for_status()

    reader = csv.reader(StringIO(r.text))
    for cols in reader:
        if len(cols) >= 4 and cols[1].strip().lower() == 'fundo':
            data_raw = cols[2].strip()
            cota_raw = cols[3].strip().replace('.', '').replace(',', '.')
            os.makedirs('data', exist_ok=True)
            payload = {
                'fundo': 'Capstone Macro FIC FIM',
                'data': data_raw,
                'cota': float(cota_raw),
            }
            with open('data/capstone.json', 'w', encoding='utf-8') as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            print(f"OK: {data_raw} | cota={cota_raw}")
            return

    print("ERRO: linha 'Fundo' nao encontrada no CSV", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
