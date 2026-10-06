<!-- DGX:ADAPTER:CLAUDE -->
<!-- DGX:COMMON-BOOTSTRAP-GRANT:START -->
BOOTSTRAP GRANT

Nada antes de ler. O soberano é o repositório `sovereign-system` (`~/Workspace/sovereign-system`); em qualquer outro
repositório do parque ele é outro repo, e aqui só mora o adaptador local. A entrada canônica é o
`protocols/bootstrap.md` do `sovereign-system`; ela aponta para a função e para a rota entregue ao harness. A
constituição, os protocolos e as specs do `sovereign-system` são a doutrina que a função deve consultar.

`reading_gate.status: COMPLETE` é a prova de que a leitura de boot foi entregue. Ausência, `INCOMPLETE` ou
`UNPROVEN` recusa a entrada com `READING_GATE_INCOMPLETE`. Este bloco prova leitura recebida; nunca é
`ExecutionGrant`, nunca concede escrita e não substitui `AUTHORIZED_WRITE`, `WRITE_SCOPE`, validação, commit ou
push.

Com o MCP conectado, a doutrina chega pelo `dgx.ready`/`dgx.read`: os caminhos de doutrina citados em qualquer
adaptador são endereço, não ordem de leitura. Não releia pelo shell (`cat`, `sed`, `rg`) o que o gate já entregou.
Shell para doutrina é fallback, só quando o MCP não entregar (sem MCP, `dgx.ready` falhou, página recusada ou
`reading_gate` sem `COMPLETE`), e o fallback é declarado no relatório. O código e os testes da missão se leem
normalmente.

O fechamento segue o `protocols/close.md` do `sovereign-system`: checkpoint transporta continuidade e Session Close
encerra quando o dono quiser. O cartão, o Envelope e o readout de close usam o mesmo nome `BOOTSTRAP GRANT`; cada
transporte continua responsável por declarar sua própria prova.

Executor headless declara a fase em que está, quando ela muda, por `dgx.round {action:"checkpoint",
structured_checkpoint:{stage, current_action, next_action, ...}}`: `READING` ao terminar o boot, `IMPLEMENTING`
antes da primeira escrita, `VALIDATING` e `GIT_CLOSING` ao fechar. O Envelope carimba a chamada exata. Fase
declarada não é entrega: a prova continua sendo Git e régua.
<!-- DGX:COMMON-BOOTSTRAP-GRANT:END -->

## Este repositório

| Fato | Valor |
|---|---|
| Tipo | Projeto público de portfólio: triagem B2B com LLM e aprovação humana em n8n |
| Surface/alias | `ai-request-triage-n8n` |
| Domínio público | Nenhum; repositório público no GitHub |
| Stack | n8n (export JSON), PostgreSQL (SQL), Python (evals) |
| Runtime/dev | O fluxo roda na VPS (`digytron-vps/automations/triage-v2`); aqui ficam só o export sanitizado, o SQL e os evals |
| Publish alias | Nenhum |
| Cliente servido | Recrutadores e o próprio dono |
| Status | Ativo; vídeo demo linkado no README |

## Comandos locais

- Evals com modelo simulado: `python3 evals/run-evals.py`

## Mapa local

- `workflows/triage-v2.export.json`: os três workflows, sem segredo.
- `db/`: schema e seed sintéticos.
- `evals/`, `fixtures/`, `prompt/`: avaliação, cenários e prompt versionado.

## Armadilhas locais

- Repositório público: nada de segredo, caminho local, dado pessoal ou cliente real; tudo é sintético.
- Claim só com prova medida (README §Results); "Vértice IA" é empresa fictícia.
