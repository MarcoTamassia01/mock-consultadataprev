import os
import csv

from constants.utils_constants import CAMINHO_CSV


def carregar_dados_csv():
    if not os.path.exists(CAMINHO_CSV):
        print(f"ERRO: Arquivo {CAMINHO_CSV} não encontrado!")
        return []
    dados = []
    with open(CAMINHO_CSV, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=';')
        reader.fieldnames = [c.strip().replace('"', '') for c in reader.fieldnames]
        for row in reader:
            clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
            dados.append(clean_row)
    return dados
