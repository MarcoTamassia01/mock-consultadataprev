# Mock de exclusão de consignado

Rota: `PUT /v1/emprestimos/excluir-consignado-trabalhador`.

Os cenários abaixo atendem aos 64 contratos distintos da lista recebida. Cada contrato
tem um retorno fixo; repetir uma chamada não muda o resultado. O cenário depende
somente de `numeroContrato`, mas os demais campos obrigatórios continuam sendo
validados. A operação não altera o estado do empréstimo.

## Distribuição

| Contratos | HTTP | Cenário |
| --- | --- | --- |
| `124`, `130` | 200 | Resultado verdadeiro com quatro campos de exclusão nulos |
| `125`, `129` | 412 | TA — Incompatibilidade crítica entre CPF, matrícula e empregador |
| `134`, `137` | 412 | HY — Empréstimo inexistente para operação de manutenção indicada |
| `142`, `132` | 412 | HZ — Não é possível realizar operação com o empréstimo nesta situacao |
| Demais 56 contratos abaixo | 200 | BF — Exclusão efetuada com sucesso |

Contratos com sucesso BF:

```text
133
135
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
  "numeroContrato": "133"
}
```

## HTTP 200 — sucesso BF

```json
{
  "codigoSucesso": "BF",
  "mensagem": "Exclusão efetuada com sucesso",
  "numeroContrato": "133",
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

## Configuração

Os contratos, códigos, mensagens e valores fixos dos novos cenários estão em
`constants/exclusao_constants.py`. A rota e os modelos de resposta estão em
`main.py`. O Swagger (`/docs`) descreve os dois formatos de HTTP 200 e o HTTP 412.
