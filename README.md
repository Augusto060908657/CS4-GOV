# Forzy – Produto Analítico Governado e Operação Contínua

**FIAP · Tecnólogo em Inteligência Artificial · Governança em IA · Challenge Sprint 4**
Octavio Augusto Ramalho Brandão Pires – RM 555696

[![gates](../../actions/workflows/gates.yml/badge.svg)](../../actions/workflows/gates.yml)

## 1. Visão geral

A Forzy é uma plataforma de monitoramento preditivo de motores elétricos industriais. Este repositório reúne os artefatos
de governança da Sprint 4: o **Metric Contract** versionado (SemVer), o motor de classificação com **Circuit Breaker**,
os **gates de promoção** (MAT, Golden Dataset, Linter Semântico e varredura de segredos), o assistente conversacional
governado (simulado), SLOs/error budget, o postmortem do incidente simulado INC-2026-001 e a documentação viva.

> Todos os dados são **simulados**. Nada aqui representa operação em produção. Os thresholds são de referência para um
> motor de indução trifásico de 45 kW (ISO 10816-3 / 20816-1, Classe II) e devem ser conferidos com o manual do fabricante
> e a edição vigente da norma antes de qualquer uso real.

## 2. Contrato vigente

| Item | Valor |
|---|---|
| Arquivo | [`metric_contract.yaml`](metric_contract.yaml) |
| Versão | **1.1.0** (MINOR, 26/11/2026) |
| Aprova | Engenheiro de Confiabilidade |
| Mantém | Data Product Owner |
| Histórico | [`CHANGELOG.md`](CHANGELOG.md) |

A v1.1.0 adiciona as regras `out_of_range` e `flatline` (ação corretiva do INC-2026-001), `plausible_range`, e os blocos
`handoff`, `assistant` e `slo`, sem alterar thresholds (por isso MINOR).

## 3. Como executar

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/run_gates.py      # roda os 4 gates; retorna código != 0 se algum falhar
python -m pytest -q              # testes (MAT, Golden Dataset, Linter, segredos)
jupyter notebook notebooks/CS4_Governanca_Forzy.ipynb   # simulação completa (seed fixa = 42)
```

No Google Colab: abra o notebook (link na seção 7) e use *Executar tudo*. O notebook é autocontido (o contrato vai embutido).
Opcional: defina `FORZY_AUDIT_SALT` para a pseudonimização do log de auditoria; sem ela, o notebook gera um salt efêmero.

## 4. Estrutura de pastas

```
.
├── metric_contract.yaml          # Metric Contract v1.1.0 (fonte da verdade)
├── CHANGELOG.md                  # histórico SemVer
├── CONTRIBUTING.md               # regras para contribuir
├── src/forzy/engine.py           # motor, Circuit Breaker, Linter e gates (extraído do notebook)
├── scripts/run_gates.py          # executa os 4 gates (usado no CI)
├── tests/test_gates.py           # testes automatizados
├── notebooks/                    # notebook técnico da Sprint 4
├── evidence/                     # CSVs gerados pelo notebook (log de auditoria e SLOs simulados)
├── docs/
│   ├── Forzy_Challenge_Sprint_4_Final.docx   # documentação final
│   ├── squad-devdata.md          # papéis do squad e o que cada um NÃO faz
│   ├── glossary.md               # perfis, TAGs e termos
│   ├── runbooks/incident-response.md
│   ├── postmortems/INC-2026-001.md
│   └── decisions/                # registros de decisão (ADRs)
└── .github/
    ├── CODEOWNERS                # responsável por pasta
    └── workflows/gates.yml       # CI: gates a cada push/PR
```

## 5. Runbook de incidente

Resumo (completo em [`docs/runbooks/incident-response.md`](docs/runbooks/incident-response.md)):

- Anomalia nos dados: resposta em até **2 horas**. Sensor desconectado (3 leituras ausentes): até **30 minutos**.
- A IA só monitora, registra alertas WARNING e aumenta a frequência de amostragem. **Parada de motor, troca de componente
  e ajuste de threshold exigem aprovação humana** (`ai_can_shutdown_motor: false`).
- Rollback de versão (meta de 15 min): suspender promoção → reverter flags → rodar Golden Dataset → publicar banner e
  changelog → abrir postmortem.
- Incidente de referência: [`INC-2026-001`](docs/postmortems/INC-2026-001.md) (zeros em sensor de temperatura; 117 de 216 min de error budget).

## 6. Glossário

Perfis, TAGs (`MOT-001-SBC`, padrão `^MOT-[0-9]{3}-[A-Z]{3}$`) e termos: [`docs/glossary.md`](docs/glossary.md).

## 7. Links

- Notebook técnico da Sprint 4 (Colab): https://colab.research.google.com/drive/1Prs7WQJpk-pJ0PQPCP02sg33OhTnxBFi?usp=sharing
- Notebook técnico da Sprint 3 (Colab): https://colab.research.google.com/drive/1PLzm5f6hijI6Vc2MJv_yaIfQ5x1x8CPM?usp=sharing
- Vídeo de defesa da Sprint 4: _**TODO: colar o link do YouTube**_
- Vídeo de defesa da Sprint 3: https://youtu.be/OKPu44CNMqY
- Vídeo da Sprint 2: https://youtu.be/91ttnnrpxKE

## 8. Squad e documentação viva

Os cinco papéis do squad (Data Product Owner, Data Engineer, Data Analyst/Scientist, Quality Engineer e DevData Coach) estão
mapeados com o que cada um **não** faz em [`docs/squad-devdata.md`](docs/squad-devdata.md). O Princípio 7 (evitar o heroísmo)
é aplicado com este README, o contrato em YAML com changelog, o notebook reprodutível, os runbooks/postmortems/ADRs e o
CODEOWNERS. Por ser trabalho individual, a separação é de responsabilidade declarada.

## 9. Pendências conhecidas

Integração com sensores IoT reais, calibração dos thresholds com dados de fabricante, indicador de flatline no painel,
checklist formal de modos de falha e registro do postmortem no changelog (ver seção 18.3 do documento).

## 10. Como contribuir

Veja [`CONTRIBUTING.md`](CONTRIBUTING.md). Resumo: branch → atualizar versão/changelog se tocar o contrato → rodar gates →
PR revisado por papel diferente do autor.
