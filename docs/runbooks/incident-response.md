# Runbook de incidente – Forzy

Aplica-se a anomalia nos dados, sensor desconectado ou suspeita de dado inválido exibido como normal.
A Forzy **não** é a camada de proteção do motor: relés e proteções locais continuam atuando.

## 1. Detectar
- Painel de observabilidade (Integridade) ou relato do operador.
- Alerta `CRITICAL`: painel + SMS/push ao engenheiro. `WARNING`: painel.

## 2. Handoff humano (valores do `metric_contract.yaml`, bloco `handoff`)
| Situação | Prazo de resposta |
|---|---|
| Anomalia nos dados (revisão de aviso) | até 2 horas |
| Sensor desconectado (3 leituras consecutivas ausentes) | até 30 minutos |

## 3. Decidir
- A IA atua sozinha apenas em: `monitorar`, `registrar_alerta_warning`, `aumentar_frequencia_amostragem`.
- Exigem aprovação humana: `parada_de_motor`, `troca_de_componente`, `ajuste_de_threshold`.
- `ai_can_shutdown_motor: false`.
- Registrar quem decidiu e o que decidiu (aceitou, rejeitou ou escalou) no mesmo Trace ID.

## 4. Conter
- Marcar o dado como inválido; manter alertas travados pelo Circuit Breaker.
- A autonomia plena só retorna após 3 leituras válidas consecutivas.

## 5. Se envolver uma nova versão (contrato, modelo ou base de conhecimento) – rollback
Meta proposta: até 15 minutos.
1. Suspender a promoção.
2. Reverter as feature flags para as versões anteriores (fixadas por tag).
3. Executar o Golden Dataset na versão restaurada (`python scripts/run_gates.py`).
4. Publicar o banner e a entrada de changelog.
5. Abrir postmortem em `docs/postmortems/`.

## 6. Error budget
Consulte a política (Tabela 19 do documento): < 50% Normal; 50–74% Atenção (postmortem obrigatório); 75–99% Restrição (só PATCH e correções); ≥ 100% congelamento de features.
