# Glossário

## Perfis (iguais em todas as sprints e no `metric_contract.yaml`)
- **Operador de Manutenção**: vê status e recomendação sintética da linha alocada; sem RUL e sem séries brutas.
- **Engenheiro de Confiabilidade**: telemetria, séries, RUL e thresholds do setor; aprova o contrato.
- **Auditor de Governança/TI**: logs e trilhas em leitura; sem telemetria.
- **Data Scientist (Admin)**: documentação técnica do modelo e dados de treino em sandbox.

## TAGs
- Padrão: `^MOT-[0-9]{3}-[A-Z]{3}$`. TAG de exemplo: `MOT-001-SBC`.

## Termos
- **Circuit Breaker**: subordina a liberação de alertas à confiabilidade do dado. Estados: CLOSED → OPEN → HALF_OPEN → CLOSED (3 leituras válidas).
- **Flatline**: valor constante por 10 leituras (epsilon 0,01), tratado como incerteza desde a v1.1.0.
- **MAT**: Metric Acceptance Test. **Golden Dataset**: casos congelados de regressão.
- **Medallion**: camadas Bronze (bruto), Silver (validado) e Gold (KPIs, alertas, base do RAG).
- **Error budget**: 0,5% de 43.200 min (30 dias) = 216 min.
- **Canary Deploy**: nova versão ativada primeiro em uma linha piloto.
- **Trace ID**: identificador que liga recomendação, resposta e decisão do operador no log de auditoria.
