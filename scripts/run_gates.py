"""Executa os 4 gates de promocao do Metric Contract e retorna codigo != 0 se algum falhar.

Uso: python scripts/run_gates.py [caminho_do_contrato]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from forzy.engine import (carregar_contrato, linter_semantico, gate_mat,
                          gate_golden, varrer_segredos)


def main(caminho="metric_contract.yaml"):
    texto = Path(caminho).read_text(encoding="utf-8")
    contrato = carregar_contrato(caminho)
    versao = contrato["contract"]["version"]

    ok_mat, _ = gate_mat(contrato)
    ok_gold, res = gate_golden(contrato, versao)
    erros = linter_semantico(contrato)
    segredos = varrer_segredos(texto)

    gates = [("Gate 1 - MAT", ok_mat),
             ("Gate 2 - Golden Dataset", ok_gold),
             ("Gate 3 - Linter Semantico", not erros),
             ("Gate 4 - Varredura de segredos", not segredos)]
    print(f"Metric Contract v{versao}")
    for nome, ok in gates:
        print(f"  [{'OK' if ok else 'FALHA'}] {nome}")
    for e in erros:
        print("    linter:", e)
    for nome, ok in res.items():
        if not ok:
            print("    golden falhou:", nome)
    aprovado = all(ok for _, ok in gates)
    print("Decisao:", "PROMOVER (iniciar Canary em 1 linha)" if aprovado else "BLOQUEAR")
    return 0 if aprovado else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
