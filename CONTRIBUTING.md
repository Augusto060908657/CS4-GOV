# Como contribuir

1. Crie um branch a partir de `main` (`feat/...`, `fix/...`, `docs/...`).
2. Se a mudança toca `metric_contract.yaml`:
   - classifique como MAJOR, MINOR ou PATCH (ver `CHANGELOG.md`);
   - atualize `contract.version`, `contract.last_updated` e o topo do bloco `changelog`
     (o Linter Semântico reprova se o topo do changelog diferir da versão);
   - atualize `CHANGELOG.md`.
3. Rode localmente: `python -m pytest -q` e `python scripts/run_gates.py`.
4. Abra um Pull Request. O CI executa os 4 gates (MAT, Golden Dataset, Linter, segredos).
5. A revisão deve ser feita por **papel diferente do autor** (ver `docs/squad-devdata.md`).
   Mudança MAJOR exige parecer do Quality Engineer e do Engenheiro de Confiabilidade.
6. Nunca versione segredos, tokens ou dados reais de planta. Os dados deste repositório são simulados.
7. Todo incidente gera um postmortem sem atribuição de culpa em `docs/postmortems/`.
