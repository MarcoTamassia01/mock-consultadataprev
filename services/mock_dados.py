from random import randint
from utils.conversor_dados import to_int, to_float

def mapear_pagamento_csv(item):
    # Usamos .get() com o nome exato da coluna da planilha
    return {
        "id": to_int(item.get("id")),
        "codigoIF": to_int(item.get("codigol")),
        "contrato": str(item.get("contrat", "")).strip(),
        "valorParcelaPaga": to_float(item.get("valorParcelaPaga")),
        "dataHoraPagamentoGuia": str(item.get("dataHoraPagamentoGuia", "")).strip(),
        "dataHoraInclusaoDataprev": str(item.get("dataHoraInclusaoDataprev", "")).strip(),
        "dataHoraRepasseIF": str(item.get("dataHoraRepasseIF", "")).strip(),
        "numeroGuia": to_int(item.get("numeroGuia")),
        "competencia": to_int(item.get("competencia")),
        "nsu": to_int(item.get("nsu"))
    }

def gerar_mock_pagamento():
    """Gera dados aleatórios caso precise de mais páginas."""
    return {
        "id": randint(2446612, 2446999),
        "codigoIF": 393,
        "contrato": "10001",
        "valorParcelaPaga": 300.50,
        "dataHoraPagamentoGuia": "01012026130000",
        "dataHoraInclusaoDataprev": "25022026094129",
        "dataHoraRepasseIF": "01012026130000",
        "numeroGuia": 56,
        "competencia": 202602,
        "nsu": 123
    }