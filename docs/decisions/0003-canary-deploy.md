# ADR 0003 – Canary Deploy como padrão de resiliência
- **Status:** aceita
- **Decisão:** nova versão ativa primeiro em uma linha piloto (ex.: linha A de Usinagem), em paralelo à estável, por período a definir (proposta: 72 h). Avança se não consumir error budget adicional nem violar escopo.
- **Motivo:** o custo de um alerta errado em ambiente industrial torna preferível limitar o alcance de uma regressão. Retry com Backoff (3 tentativas, espera exponencial com jitter) fica como complemento para falhas transitórias de ingestão.
