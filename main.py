
from random import randint
from fastapi import FastAPI, Query
from constants.utils_constants import  QUANTIDADE_TOTAL_PAGINAS, QUANTIDADE_POR_PAGINA
from utils.carregar_dados import carregar_dados_csv
from utils.conversor_dados import to_int, to_float

app = FastAPI()

def mapear_pagamento_csv(item):
    return {
        "id": to_int(item.get("id")),
        "codigoIF": to_int(item.get("codigol") or item.get("codigoIF")),  # Tenta os dois nomes
        "contrato": str(item.get("contrat") or item.get("contrato") or "").strip(),
        "valorParcelaPaga": to_float(item.get("valorParcelaPaga")),
        "dataHoraPagamentoGuia": item.get("dataHoraPagamentoGuia", ""),
        "dataHoraInclusaoDataprev": item.get("dataHoraInclusaoDataprev", ""),
        "dataHoraRepasseIF": item.get("dataHoraRepasseIF", ""),
        "numeroGuia": to_int(item.get("numeroGuia")),
        "competencia": to_int(item.get("competencia")),
        "nsu": to_int(item.get("nsu"))
    }


# --- ENDPOINT ---
@app.get("/v1/emprestimos/repasse-pagamentos")
def get_pagamentos(
        dataHoraInicio: str = Query("22022026000000"),
        dataHoraFim: str = Query("25022026094600"),
        nroPagina: int = Query(1)
):
    # 1. Carrega todos os dados do CSV (ex: as 70 linhas)
    registros_csv = carregar_dados_csv()
    conteudo_csv = [mapear_pagamento_csv(item) for item in registros_csv]

    # 2. Descobre o último ID para fazer o sequencial
    if conteudo_csv:
        ultimo_id = max(item["id"] for item in conteudo_csv)
    else:
        ultimo_id = 2446611  # Valor base caso o CSV esteja vazio

    # 3. Gera as 100 linhas de mock sequenciais
    conteudo_mock = []
    for i in range(1, 101):
        conteudo_mock.append({
            "id": ultimo_id + i,  # Sequencial: sempre +1
            "codigoIF": 393,
            "contrato": "999",  # Fixo conforme pedido
            "valorParcelaPaga": 1010,  # Fixo conforme pedido
            "dataHoraPagamentoGuia": "01012026130000",
            "dataHoraInclusaoDataprev": "25022026094129",
            "dataHoraRepasseIF": "01012026130000",
            "numeroGuia": 56,
            "competencia": 202602,
            "nsu": 123
        })

    # 4. Junta tudo em uma lista mestre
    lista_completa = conteudo_csv + conteudo_mock

    # 5. Lógica de Paginação sobre a lista completa
    inicio = (nroPagina - 1) * QUANTIDADE_POR_PAGINA
    fim = inicio + QUANTIDADE_POR_PAGINA
    conteudo_paginado = lista_completa[inicio:fim]

    return {
        "nroPaginaAtual": nroPagina,
        "nroTotalPaginas": (len(lista_completa) // QUANTIDADE_POR_PAGINA) + 1,
        "nroTotalRegistros": len(lista_completa),
        "qtdRegistrosPorPagina": QUANTIDADE_POR_PAGINA,
        "qtdRegistrosPaginaAtual": len(conteudo_paginado),
        "dataHoraInicio": dataHoraInicio,
        "dataHoraFim": dataHoraFim,
        "conteudo": conteudo_paginado
    }