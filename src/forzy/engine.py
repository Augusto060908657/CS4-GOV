"""Motor de classificacao, Circuit Breaker e gates da Plataforma Forzy.

Extraido do notebook da Sprint 4 (notebooks/CS4_Governanca_Forzy.ipynb) para
que os gates rodem no CI sem Jupyter. Logica identica a do notebook.
"""
import re
import numpy as np
import pandas as pd
import yaml

SEED = 42


def carregar_contrato(caminho="metric_contract.yaml"):
    with open(caminho, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------- Gate 3
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
GLOSSARIO_PERFIS = ["Operador de Manutenção", "Engenheiro de Confiabilidade",
                    "Auditor de Governança/TI", "Data Scientist (Admin)"]
UNIDADES_VALIDAS = {"mm/s", "degC", "g"}

def linter_semantico(c):
    erros = []
    if not SEMVER.match(str(c["contract"]["version"])):
        erros.append("versao fora do padrao SemVer")
    for nome, s in c["sensors"].items():
        lo, hi = s["plausible_range"]
        if s["unit"] not in UNIDADES_VALIDAS:
            erros.append(f"{nome}: unidade invalida ({s['unit']})")
        if not s["warning"] < s["critical"]:
            erros.append(f"{nome}: warning deve ser menor que critical")
        if not (lo < s["warning"] < s["critical"] <= hi):
            erros.append(f"{nome}: thresholds fora da faixa plausivel")
        if s["max_jump"] <= 0:
            erros.append(f"{nome}: max_jump deve ser positivo")
    ra = c["reference_asset"]
    if not re.match(ra["tag_pattern"], ra["example_tag"]):
        erros.append("TAG de exemplo nao segue o padrao de TAG")
    if c["circuit_breaker"]["valid_readings_to_close"] < 1:
        erros.append("valid_readings_to_close deve ser >= 1")
    if set(c["profiles"]) != set(GLOSSARIO_PERFIS):
        erros.append("perfis divergem do glossario (mesmos perfis das Sprints 1 a 3)")
    if c["changelog"][0]["version"] != c["contract"]["version"]:
        erros.append("topo do changelog difere da versao do contrato")
    if c["slo"]["availability_effective_pct"] >= 100:
        erros.append("SLO de disponibilidade em 100% nao gera error budget")
    return erros



# ------------------------------------------------------ Motor / Circuit Breaker
def _vtuple(v):
    return tuple(int(x) for x in v.split("."))

def _falt(x):
    return x is None or (isinstance(x, float) and np.isnan(x))

def avaliar_sensor(valores, sensor, contrato, versao_regras="1.1.0", ativo_legado=False):
    s, cb, an = contrato["sensors"][sensor], contrato["circuit_breaker"], contrato["anomaly"]
    warn, crit = s["warning"], s["critical"]
    if ativo_legado:  # tolerancia de 10% apenas para o limiar critico (Sprint 1)
        crit = crit * (1 + contrato["reference_asset"]["legacy_asset_tolerance_critical_pct"] / 100)
    novo = _vtuple(versao_regras) >= (1, 1, 0)
    vals = list(valores)
    estado, validas, hist_ok, linhas = "CLOSED", 0, [], []
    for i, v in enumerate(vals):
        motivos = []
        faltante = _falt(v)
        janela = vals[max(0, i - cb["window"] + 1): i + 1]
        pct = 100 * np.mean([_falt(x) for x in janela])
        if faltante:
            motivos.append("dado_faltante")
        elif pct > cb["max_missing_pct"]:
            motivos.append("janela_com_faltantes")
        if not faltante and i > 0 and not _falt(vals[i - 1]) and abs(v - vals[i - 1]) > s["max_jump"]:
            motivos.append("salto_implausivel")
        if novo and not faltante:
            lo, hi = s["plausible_range"]
            if v < lo or v > hi:
                motivos.append("fora_da_faixa")
            fl = cb["rules"]["flatline"]
            w = vals[max(0, i - fl["window"] + 1): i + 1]
            if len(w) == fl["window"] and not any(_falt(x) for x in w) and (max(w) - min(w)) <= fl["epsilon"]:
                motivos.append("flatline")
        if motivos:
            estado, validas, liberado = "OPEN", 0, False
        elif estado == "CLOSED":
            liberado = True
        else:
            validas += 1
            if validas >= cb["valid_readings_to_close"]:
                estado, validas, liberado = "CLOSED", 0, True
            else:
                estado, liberado = "HALF_OPEN", False
        if faltante:
            classe = "SEM_DADO"
        else:
            classe = "CRITICAL" if v >= crit else ("WARNING" if v >= warn else "NORMAL")
            if classe == "NORMAL" and liberado and len(hist_ok) >= an["min_history"]:
                h = hist_ok[-an["history_window"]:]
                sd = np.std(h, ddof=1)
                if sd > 0 and abs(v - np.mean(h)) / sd >= an["zscore_threshold"]:
                    classe = "ANOMALIA_ESTATISTICA"
        if not motivos and not faltante:
            hist_ok.append(v)
        linhas.append(dict(idx=i, valor=v, classe=classe, estado_breaker=estado,
                           motivos=",".join(motivos), alerta_liberado=liberado,
                           alerta_final=classe if liberado else "TRAVADO_CIRCUIT_BREAKER"))
    return pd.DataFrame(linhas)


# ---------------------------------------------------------------- Gate 1 (MAT)
CASOS_MAT = [  # (sensor, valor, ativo_legado, classe_esperada)
    ("vibracao", 2.0, False, "NORMAL"), ("vibracao", 4.5, False, "WARNING"),
    ("vibracao", 7.09, False, "WARNING"), ("vibracao", 7.1, False, "CRITICAL"),
    ("vibracao", 7.5, True, "WARNING"), ("vibracao", 7.9, True, "CRITICAL"),
    ("temperatura", 74.9, False, "NORMAL"), ("temperatura", 75.0, False, "WARNING"),
    ("temperatura", 95.0, False, "CRITICAL"),
    ("aceleracao", 1.99, False, "NORMAL"), ("aceleracao", 2.0, False, "WARNING"),
    ("aceleracao", 3.5, False, "CRITICAL"),
]


def gate_mat(contrato):
    linhas = []
    for sensor, valor, leg, esperado in CASOS_MAT:
        obtido = avaliar_sensor([valor], sensor, contrato, ativo_legado=leg).loc[0, "classe"]
        linhas.append(dict(sensor=sensor, valor=valor, ativo_legado=leg, esperado=esperado,
                           obtido=obtido, ok=obtido == esperado))
    df = pd.DataFrame(linhas)
    return bool(df["ok"].all()), df


# ------------------------------------------------------- Gate 2 (Golden Dataset)
def golden_cases():
    g = {}
    r = np.random.default_rng(2)
    g["G1_operacao_normal"] = dict(sensor="vibracao", serie=list(2.2 + r.normal(0, 0.1, 40)))
    r = np.random.default_rng(SEED)
    s = list(2.2 + r.normal(0, 0.1, 30)); s[10:15] = [15.0, 0.1, 14.0, 2.25, 2.40]
    g["G2_dados_ruins_sprint3"] = dict(sensor="vibracao", serie=s)
    r = np.random.default_rng(3)
    s = list(2.2 + r.normal(0, 0.1, 20)) + list(np.linspace(2.8, 8.4, 11)) + [8.4] * 4
    g["G3_degradacao_real"] = dict(sensor="vibracao", serie=s)
    g["G4_temperatura_zeros"] = dict(sensor="temperatura", serie=[71.0 + 0.3 * ((i * 7) % 5 - 2) / 2 for i in range(30)] + [0.0] * 40 + [71.0 + 0.1 * (i % 3) for i in range(10)])
    r = np.random.default_rng(5)
    g["G5_flatline_valor_plausivel"] = dict(sensor="temperatura", serie=list(72 + r.normal(0, 0.3, 20)) + [71.30] * 25)
    return g


def checar_golden(contrato, versao):
    g, res = golden_cases(), {}
    for nome, c in g.items():
        r = avaliar_sensor(c["serie"], c["sensor"], contrato, versao_regras=versao)
        fin, v = r["alerta_final"], r["valor"]
        if nome == "G1_operacao_normal":
            ok = bool((fin == "NORMAL").all())
        elif nome == "G2_dados_ruins_sprint3":
            ok = list(r.index[fin == "TRAVADO_CIRCUIT_BREAKER"]) == [10, 11, 12, 13, 14, 15]
        elif nome == "G3_degradacao_real":
            crit_idx = [i for i, x in enumerate(c["serie"]) if x >= 7.1]
            ok = (not (fin == "TRAVADO_CIRCUIT_BREAKER").any()) and all(fin[i] == "CRITICAL" for i in crit_idx)
        elif nome == "G4_temperatura_zeros":
            ok = all(fin[i] == "TRAVADO_CIRCUIT_BREAKER" for i in range(30, 70))
        elif nome == "G5_flatline_valor_plausivel":
            ok = list(r.index[fin == "TRAVADO_CIRCUIT_BREAKER"]) == list(range(29, 45))
        res[nome] = ok
    return res


def gate_golden(contrato, versao="1.1.0"):
    res = checar_golden(contrato, versao)
    return all(res.values()), res


# ----------------------------------------------------- Gate 4 (varredura de segredos)
PADROES = [r"(?i)(password|senha|passwd)\s*[:=]\s*\S+",
           r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*\S{8,}",
           r"(?i)bearer\s+[A-Za-z0-9\-_\.]{20,}",
           r"AKIA[0-9A-Z]{16}",
           r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"]


def varrer_segredos(texto):
    return [p for p in PADROES if re.search(p, texto)]
