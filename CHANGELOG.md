# Changelog

Segue [Versionamento Semântico](https://semver.org/lang/pt-BR/). O changelog do contrato
(`metric_contract.yaml`, bloco `changelog`) é a fonte; este arquivo o espelha para leitura.

| Tipo | Quando | Exigência |
|---|---|---|
| MAJOR | Altera threshold crítico, remove/renomeia sensor, muda semântica de classe ou escopo de perfil | Banner de Ruptura + plano de rollback |
| MINOR | Adiciona sensor, regra ou campo sem alterar o que já existe | Gates + Canary |
| PATCH | Correção de texto, comentário ou documentação | Gates |

## [1.1.0] – 2026-11-26 – MINOR
- Adiciona as regras de Circuit Breaker `out_of_range` e `flatline` (ação corretiva do INC-2026-001).
- Adiciona `plausible_range` por sensor.
- Adiciona os blocos `handoff`, `assistant` e `slo`.
- Padroniza a TAG de exemplo como `MOT-001-SBC`.
- Não altera thresholds nem classes de leitura (por isso MINOR).

## [1.0.0] – 2026-08-31 – MAJOR
- Versão inicial formalizada na Sprint 3: thresholds de vibração, temperatura e aceleração.
- Circuit Breaker com janela, percentual de faltantes e salto implausível.
- Detecção estatística por z-score.
