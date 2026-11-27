# ADR 0002 – Primeiro Quality Gate na promoção Bronze → Silver
- **Status:** aceita
- **Contexto:** no INC-2026-001, zeros aceitos na fronteira foram exibidos como NORMAL.
- **Decisão:** o Gate 1 valida esquema, unidades, timestamps, faltantes, saltos, faixa plausível, flatline e OCR_Confidence (< 0,90 exige validação humana) antes da Silver.
- **Consequências:** dado inválido não chega às regras de classificação, KPIs, alertas nem ao contexto do assistente (menor custo de contenção).
