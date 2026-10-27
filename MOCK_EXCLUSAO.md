# Mock de exclusão de consignado

Rota: `PUT /v1/emprestimos/excluir-consignado-trabalhador`.

O lote inicial contém 76 contratos distintos. O lote da planilha acrescenta outros
30 contratos, descritos na seção específica abaixo. Cada contrato
tem um retorno fixo; repetir uma chamada não muda o resultado. O cenário depende
somente de `numeroContrato`, mas os demais campos obrigatórios continuam sendo
validados. A operação não altera o estado do empréstimo.

## Distribuição do lote inicial (76 contratos)

| Contratos | HTTP | Cenário |
| --- | --- | --- |
| `124`, `130` | 200 | Resultado verdadeiro com quatro campos de exclusão nulos |
| `125`, `129`, `1000000067` | 412 | TA — Incompatibilidade crítica entre CPF, matrícula e empregador |
| `134`, `137`, `1000000069` | 412 | HY — Empréstimo inexistente para operação de manutenção indicada |
| `142`, `132`, `1000000070` | 412 | HZ — Não é possível realizar operação com o empréstimo nesta situacao |
| `133`, `6081` | 404 | Contrato já cancelado ou não localizado, com `code`, `error` e `message` |
| `135` | 500 | Erro interno genérico no formato `erros` |
| Demais 62 contratos abaixo | 200 | BF — Exclusão efetuada com sucesso |

Contratos com sucesso BF:

```text
136
141
149
131
146
148
100112
100111
100113
900044
100177
100144
100147
100146
100142
100143
100178
100180
10002
10061
10062
10003
158
159
116
156
157
117
900045
1000000060
1000000061
100228
100195
100239
1000000056
1000000059
902671
62
100000
100179
900039
1000000001
100238
10058
10059
1000000009
1000000046
100196
100221
1000000006
120
900036
50004
50005
1000000068
100019
100017
100022
100020
100018
6086
6091
```

Os contratos cadastrados anteriormente continuam com os retornos D12/D13/D14.
Um contrato que não conste nem no cadastro anterior nem nos cenários acima retorna
HTTP 404 com `{"detail": "Empréstimo inexistente"}`.
Um body que não passe pela validação dos campos obrigatórios continua retornando HTTP 422.

## Requisição

Troque somente `numeroContrato` para selecionar outro cenário:

```json
{
  "numeroInscricaoEmpregador": "12345678000199",
  "cpfTrabalhador": 12345678901,
  "matricula": "MOCK",
  "motivoExclusao": 1,
  "numeroContrato": "136"
}
```

## HTTP 200 — sucesso BF

```json
{
  "codigoSucesso": "BF",
  "mensagem": "Exclusão efetuada com sucesso",
  "numeroContrato": "136",
  "hashOperacao": 71295845,
  "competenciaExclusao": 102026
}
```

O contrato é copiado da requisição, removendo espaços nas extremidades.
O hash e a competência são fixos, seguindo o exemplo fornecido.
A competência deste cenário está em MMAAAA (`102026`); o formato dos retornos
dos contratos antigos permanece inalterado.

## HTTP 200 — campos nulos

```json
{
  "resultado": true,
  "mensagem": "Consignado excluído com sucesso na DataPrev",
  "contrato": "124",
  "codigoSucesso": null,
  "numeroContrato": null,
  "competenciaExclusao": null,
  "hashOperacao": null
}
```

O contrato recebido aparece em `contrato`; os quatro campos nulos são mantidos
explicitamente no JSON.

## HTTP 412 — TA

```json
{
  "erros": [
    {
      "codigo": "TA",
      "mensagem": "Incompatibilidade crítica entre CPF, matrícula e empregador"
    }
  ]
}
```

## HTTP 412 — HY

```json
{
  "numeroContrato": "134",
  "erros": [
    {
      "codigo": "HY",
      "mensagem": "Empréstimo inexistente para operação de manutenção indicada"
    }
  ]
}
```

## HTTP 412 — HZ

```json
{
  "numeroContrato": "142",
  "erros": [
    {
      "codigo": "HZ",
      "mensagem": "Não é possível realizar operação com o empréstimo nesta situacao"
    }
  ]
}
```

As mensagens seguem o catálogo fornecido. TA não inclui `numeroContrato`;
HY e HZ incluem o contrato recebido. Todos os três erros de cenário usam HTTP 412.

## HTTP 404 — contratos 133, 6081, 837 e 839

```json
{
  "code": "404",
  "error": "Not Found",
  "message": "Tentativa de excluir/cancelar contrato que já foi cancelado ou não localizado."
}
```

Este corpo é específico dos contratos `133`, `6081`, `837` e `839`. Contratos fora do cadastro continuam
com o corpo HTTP 404 `{"detail": "Empréstimo inexistente"}`.

## HTTP 500 — contratos 135, 843 e 841

```json
{
  "erros": [
    {
      "codigo": "500",
      "mensagem": "Erro interno do servidor."
    }
  ]
}
```

É uma resposta de erro simulada e fixa, no mesmo formato `erros` dos cenários
existentes. O contrato `135` foi preservado; o lote da planilha acrescenta os
contratos `843` e `841` para os dois novos exemplos de HTTP 500.

## Lote da planilha (30 contratos)

Fonte: coluna `OPERACION` de `MASSA-DADOS-EXCLUIR-DATAPREV-V.xlsx`.
Foram selecionados 15 números da aba `CANCELADOS` (`D9:D23`) e 15 da aba
`LIQUIDADOS` (`D2:D16`), todos distintos e sem alterar contratos já cadastrados.
A planilha foi apenas lida; as situações abaixo são cenários simulados do mock.

| Contratos | HTTP | Cenário |
| --- | --- | --- |
| 16 contratos listados abaixo | 200 | BF — Exclusão efetuada com sucesso |
| `801`, `804` | 200 | Resultado verdadeiro com quatro campos nulos |
| `813`, `822` | 412 | TA |
| `823`, `825` | 412 | HY |
| `828`, `829` | 412 | HZ |
| `837`, `839` | 404 | Personalizado: `code`, `error`, `message` |
| `840`, `842` | 404 | Padrão simulado: `{"detail": "Empréstimo inexistente"}` |
| `843`, `841` | 500 | Erro interno do servidor, no formato `erros` |

Contratos do lote com sucesso BF:

```text
92621663
92622099
99409837
99410829
99411547
99450977
99452666
93848464
93850121
93850345
92564449
92564922
99450588
99451210
99451967
256
```

São 18 respostas HTTP 200 (16 BF e 2 com nulos) e 12 respostas de erro.
Os contratos `840` e `842` estão cadastrados especificamente para simular o corpo
do 404 padrão; os demais contratos desconhecidos mantêm o comportamento anterior.

HTTP 422 é uma validação da requisição e não um cenário escolhido pelo contrato.
Para testar dois exemplos usando os mesmos 30 números:

- Envie `92621663` sem o campo obrigatório `matricula`.
- Envie `92622099` com `cpfTrabalhador` igual a `"INVALIDO"`.

Com o body válido, esses dois contratos continuam retornando HTTP 200 / BF.
As duas requisições inválidas estão prontas em `test_main.http`.

## Configuração

Os contratos, códigos, mensagens e valores fixos dos novos cenários estão em
`constants/exclusao_constants.py`. A rota e os modelos de resposta estão em
`main.py`. O Swagger (`/docs`) descreve os dois formatos de HTTP 200, as duas
variantes de HTTP 404 e os erros HTTP 412 e HTTP 500.
