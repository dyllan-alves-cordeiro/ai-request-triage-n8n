---
id: ai-request-triage-n8n.docs.dgx-agent-md
role: ponteiro-local-para-a-doutrina-v2-do-soberano-o-bloco-comum-e-ca
layer: docs
kind: authored
provenance: AUTHORED_MEANING
owner: docs
status: active
surface: ai-request-triage-n8n
plane: doc
summary: "Ponteiro local para a doutrina V2 do soberano; o bloco comum e carimbado pelo LIAM."
---
<!-- DGX:ANCHOR: dgx-agent-bootstrap-pointer -->


# DGX-AGENT.md — ponteiro para o Soberano V2

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

Leia `AGENTS.md` na raiz deste repositório. O bloco comum fica carimbado pelo
LIAM; os fatos locais pertencem aos três gêmeos.
