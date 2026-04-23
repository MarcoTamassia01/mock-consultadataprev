
from fastapi import Body, FastAPI, Query
from constants.utils_constants import QUANTIDADE_POR_PAGINA
from utils.carregar_dados import carregar_dados_csv
from utils.conversor_dados import to_int, to_float
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "ok"}

class ExcluirConsignadoRequest(BaseModel):
    numeroInscricaoEmpregador: int = Field(..., ge=0)
    cpfTrabalhador: int = Field(..., ge=0)
    matricula: str
    motivoExclusao: int
    numeroContrato: str


class ExcluirConsignadoResponse(BaseModel):
    codigoSucesso: str
    mensagem: str
    numeroContrato: str
    hashOperacao: int
    competenciaExclusao: int


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


@app.get("/v1/emprestimos/emprestimo-trabalhador")
def get_emprestimo_trabalhador(
    numeroContrato: str = Query(..., min_length=1),
):
    contrato = str(numeroContrato).strip()
    contrato_int = to_int(contrato)

    def _mock_for_contrato(contrato_str: str) -> dict:
        base_cnpj = 3495672000103
        contrato_num = to_int(contrato_str) or 70000001
        suffix = contrato_num % 10000
        cpf = int(f"287130{suffix:04d}{(suffix * 7) % 100:02d}")

        return {
            "cpf": cpf,
            "matricula": str(cpf),
            "numeroInscricaoEmpregador": base_cnpj + (contrato_num % 97),
            "nomeTrabalhador": f"Fulano {cpf}",
            "nomeEmpregador": "string",
            "totalParcelas": 18 + (contrato_num % 5),
            "valorParcela": round(500 + (contrato_num % 300) + 0.11, 2),
            "valorLiberado": 10000,
        }

    mocks_por_contrato = {
        "70000001": {
            "cpf": 28713098098,
            "matricula": "28713098098",
            "numeroInscricaoEmpregador": 3495672000103,
            "nomeTrabalhador": "Fulano 28713098098",
            "nomeEmpregador": "string",
            "totalParcelas": 18,
            "valorParcela": 644.11,
            "valorLiberado": 10000,
        },
        "3697": _mock_for_contrato("3697"),
        "3735": _mock_for_contrato("3735"),
        "3743": _mock_for_contrato("3743"),
        "4287": _mock_for_contrato("4287"),
        "4341": _mock_for_contrato("4341"),
        "4358": _mock_for_contrato("4358"),
        "361": _mock_for_contrato("361"),
        "388": _mock_for_contrato("388"),
        "84": _mock_for_contrato("84"),
        "30": _mock_for_contrato("30"),
        "80": _mock_for_contrato("80"),
        "82": _mock_for_contrato("82"),
        "86": _mock_for_contrato("86"),
        "87": _mock_for_contrato("87"),
        "353": _mock_for_contrato("353"),
        "88": _mock_for_contrato("88"),
    }

    dados = mocks_por_contrato.get(contrato, _mock_for_contrato(contrato))
    cpf = dados["cpf"]
    matricula = dados["matricula"]
    cnpj = dados["numeroInscricaoEmpregador"]

    situacao_por_contrato = {
        "3697": {"codigo": 7, "descricao": "Suspenso "},
        "3735": {"codigo": 7, "descricao": "Suspenso "},
        "3743": {"codigo": 0, "descricao": "Ativo"},
        "3920": {"codigo": 15, "descricao": "ENCERRADO"},
        "4018": {"codigo": 7, "descricao": "SUSPENSO"},
        "4287": {"codigo": 8, "descricao": "Suspenso Banco"},
        "4320": {"codigo": 0, "descricao": "ATIVO"},
        "4341": {"codigo": 15, "descricao": "Encerrado por Temino de Vinculo"},
        "4358": {"codigo": 15, "descricao": "Encerrado por Temino de Vinculo"},
        "4257": {"codigo": 0, "descricao": "ATIVO"},
        "361": {"codigo": 7, "descricao": "Suspenso "},
        "388": {"codigo": 7, "descricao": "Suspenso "},
        "84": {"codigo": 8, "descricao": "Suspenso Banco"},
        "30": {"codigo": 8, "descricao": "Suspenso Banco"},
        "80": {"codigo": 15, "descricao": "Encerrado por Temino de Vinculo"},
        "82": {"codigo": 15, "descricao": "Encerrado por Temino de Vinculo"},
        "86": {"codigo": 7, "descricao": "AFASTADO"},
        "87": {"codigo": 8, "descricao": "AFASTADO"},
        "353": {"codigo": 15, "descricao": "Desligado"},
        "88": {"codigo": 15, "descricao": "Desligado"},
    }
    situacao_emprestimo = situacao_por_contrato.get(
        contrato, {"codigo": 0, "descricao": "Ativo"}
    )

    return {
        "ifConcessora": {
            "codigo": 393,
            "descricao": "BANCO VOLKSWAGEN",
        },
        "contrato": contrato,
        "cpf": cpf,
        "matricula": matricula,
        "inscricaoEmpregador": {
            "codigo": 1,
            "descricao": "CNPJ",
        },
        "numeroInscricaoEmpregador": cnpj,
        "nomeTrabalhador": dados["nomeTrabalhador"],
        "nomeEmpregador": dados["nomeEmpregador"],
        "dataInicioContrato": "12022026",
        "dataFimContrato": "26042027",
        "competenciaInicioDesconto": 202603,
        "competenciaFimDesconto": 202708,
        "totalParcelas": dados["totalParcelas"],
        "valorParcela": dados["valorParcela"],
        "valorEmprestimo": 11594.08,
        "valorLiberado": dados["valorLiberado"],
        "dataHoraInclusaoEmprestimo": "18022026161526",
        "origemAverbacao": {
            "codigo": 0,
            "descricao": "Averbação banco",
        },
        "dataHoraAtualizacao": "18022026161526",
        "situacaoEmprestimo": situacao_emprestimo,
        "dataHoraEnvioInfoContrato": "24022026105905",
        "valorIOF": 297.95,
        "valorTaxaAnual": 12.55,
        "valorCetAnual": 16.11,
        "valorTaxaMensal": 0.99,
        "valorCetMensal": 1.25,
        "dataPrimeiroDesconto": "26042026",
        "cnpjOperador": cnpj,
        "informacoesContrato": {
            "arquivosEnviados": [
                {
                    "tipoArquivo": 2,
                    "descricao": "Contrato",
                }
            ],
            "ip": "10.39.124.145",
            "dataHoraAssinatura": "18022026094400",
            "indicadorAnalfabetismo": False,
            "indicadorAssinaturaCertDigitalICPBrasil": False,
            "indicadorValidacaoComDocOficial": False,
            "nsuContrato": contrato_int if contrato_int else 70000001,
            "tipoAutenticacao": 2,
        },
        "qtdPagamentos": 0,
        "qtdEscrituracoes": 0,
        "pagamentos": [],
        "escrituracoes": [],
        "parcelasAntecipadas": [],
    }


@app.post("/v1/emprestimos/excluir-consignado-trabalhador", response_model=ExcluirConsignadoResponse)
def excluir_consignado_trabalhador(payload: ExcluirConsignadoRequest = Body(...)):
    contrato = str(payload.numeroContrato).strip()

    # Mocks "diferentes" por contrato (mantendo o mesmo shape do response)
    contratos_mock = [
        "1",
        "19",
        "22",
        "25",
        "27",
        "30",
        "80",
        "82",
        "99",
        "100",
        "167",
        "175",
        "183",
        "191",
        "201",
        "202",
        "205",
        "213",
        "221",
        "230",
        "302",
        "370",
        "418",
        "450",
        "469",
        "477",
        "581",
        "582",
        "337",
        "3500",
        "3501",
        "3502",
        "3503",
        "3514",
        "3515",
        "3522",
        "3523",
        "3527",
        "3529",
        "3537",
        "3842",
        "3845",
        "3868",
        "4371",
        "4373",
        "4374",
        "4377",
        "14",
    ]
    contratos_set = set(contratos_mock)

    base_hash = 71295845
    contrato_num = to_int(contrato)
    variacao = (contrato_num or sum(ord(c) for c in contrato)) % 97

    # Variação de código/mensagem por contrato (determinística)
    codigos = ["D12", "D13", "D14"]
    codigo_sucesso = codigos[variacao % len(codigos)]
    mensagens = {
        "D12": "Exclusão registrada",
        "D13": "Exclusão recebida para processamento",
        "D14": "Exclusão registrada com ressalvas",
    }
    mensagem_base = mensagens[codigo_sucesso]

    if contrato in contratos_set:
        return {
            "codigoSucesso": codigo_sucesso,
            "mensagem": f"{mensagem_base} ({contrato})",
            "numeroContrato": contrato,
            "hashOperacao": base_hash + variacao,
            "competenciaExclusao": 202600 + (variacao % 12) + 1,
        }

    # Fallback para qualquer outro contrato (ainda útil para testes)
    return {
        "codigoSucesso": codigo_sucesso,
        "mensagem": mensagem_base,
        "numeroContrato": contrato,
        "hashOperacao": base_hash + variacao,
        "competenciaExclusao": 202601,
    }