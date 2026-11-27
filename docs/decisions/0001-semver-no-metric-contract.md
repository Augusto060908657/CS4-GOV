# ADR 0001 – Metric Contract em YAML com SemVer e changelog
- **Status:** aceita
- **Contexto:** os limiares de interpretação definem a fronteira entre ambiguidade estatística e ação automática; precisam de histórico e aprovação.
- **Decisão:** manter `metric_contract.yaml` no repositório, com SemVer (MAJOR/MINOR/PATCH) e bloco `changelog`. v1.0.0 = contrato da Sprint 3; v1.1.0 (MINOR) = regras `out_of_range`/`flatline`, `plausible_range`, blocos `handoff`, `assistant` e `slo`, sem alterar thresholds.
- **Consequências:** MAJOR exige Banner de Ruptura e plano de rollback; o Linter Semântico impede divergência entre versão e topo do changelog.
