# Squad DevData – papéis e o que está fora do escopo de cada um

Trabalho individual: os cinco papéis são acumulados pelo mesmo integrante (Octavio Augusto Ramalho Brandão Pires).
O mapeamento explicita o que cada papel **não** faz, para que a acumulação não vire decisão sem contrapeso.

| Papel | Responsabilidades | Fora do escopo |
|---|---|---|
| Data Product Owner | Prioriza o backlog, mantém o Metric Contract e comunica a Forzy. | Implementar pipelines; aprovar mudança MAJOR sem parecer do Quality Engineer. |
| Data Engineer | Estrutura pipeline Bronze, Silver e Gold, ingestão, gates no CI e gestão de segredos. | Definir thresholds; decidir prioridades; validar a própria entrega. |
| Data Analyst / Scientist | Trata modelo de RUL, fairness, painel de observabilidade e base de conhecimento do RAG. | Promover versão sem gates; alterar a matriz RBAC. |
| Quality Engineer | Executa Golden Dataset, MAT, Linter, cálculo do error budget e análise técnica do postmortem. | Corrigir o código do pipeline; definir prioridades. |
| DevData Coach | Organiza cerimônias, retrospectiva, README e documentação viva. | Tomar decisões técnicas ou de produto; aprovar entregas. |

## Como o repositório evita o heroísmo (Princípio 7 do Manifesto DataOps)

O conhecimento não fica em uma única pessoa porque está registrado no repositório e verificado por gates:

- `README.md`: visão geral, execução, estrutura, versão do contrato, runbook, glossário, links e regras de contribuição.
- `metric_contract.yaml` com changelog + `CHANGELOG.md`: regras e histórico versionados em SemVer.
- Notebook reprodutível com seed fixa (`SEED = 42`) e gates executáveis no CI.
- `docs/runbooks/`, `docs/postmortems/` e `docs/decisions/`: documentação viva mantida junto ao código (Princípio 12, conforme o enunciado da sprint).
- `.github/CODEOWNERS`: responsável por pasta; revisão por papel diferente do autor.

## Limite reconhecido

Em trabalho individual a separação de papéis é de **responsabilidade declarada**, não de pessoas distintas.
Em um squad real, cada linha acima teria um integrante diferente e o CODEOWNERS refletiria isso.
