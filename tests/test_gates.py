from pathlib import Path
import numpy as np
from forzy.engine import (carregar_contrato, linter_semantico, gate_mat, gate_golden,
                          varrer_segredos, avaliar_sensor)

RAIZ = Path(__file__).resolve().parents[1]
CONTRATO = carregar_contrato(str(RAIZ / "metric_contract.yaml"))


def test_contrato_tem_bloco_assistant():
    assert "assistant" in CONTRATO, "bloco 'assistant' ausente (chave digitada errada?)"
    assert CONTRATO["assistant"]["citation_required"] is True
    assert CONTRATO["handoff"]["ai_can_shutdown_motor"] is False


def test_versao_vigente_e_1_1_0():
    assert CONTRATO["contract"]["version"] == "1.1.0"
    assert CONTRATO["changelog"][0]["type"] == "MINOR"


def test_linter_semantico():
    assert linter_semantico(CONTRATO) == []


def test_gate_mat():
    ok, df = gate_mat(CONTRATO)
    assert ok, df[~df["ok"]]


def test_golden_v110_passa_e_v100_falha():
    ok110, _ = gate_golden(CONTRATO, "1.1.0")
    ok100, _ = gate_golden(CONTRATO, "1.0.0")
    assert ok110
    assert not ok100  # o gate teria bloqueado a v1.0.0 (INC-2026-001)


def test_zeros_de_temperatura_ficam_travados_na_v110():
    serie = [71.0] * 30 + [0.0] * 40
    r = avaliar_sensor(serie, "temperatura", CONTRATO, versao_regras="1.1.0")
    assert (r.loc[30:, "alerta_final"] == "TRAVADO_CIRCUIT_BREAKER").all()


def test_varredura_de_segredos_detecta_amostra():
    assert varrer_segredos("Authorization: Bearer " + "x" * 24)
    assert varrer_segredos(Path(RAIZ / "metric_contract.yaml").read_text(encoding="utf-8")) == []
