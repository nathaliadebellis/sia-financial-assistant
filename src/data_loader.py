import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
CONHECIMENTO_DIR = DATA_DIR / "conhecimento"
USUARIO_DIR = DATA_DIR / "usuario"


def carregar_dados():
    """Carrega os dados de conhecimento e do usuário em DataFrames."""
    return {
        "conceitos": pd.read_json(CONHECIMENTO_DIR / "conceitos_financeiros.json"),
        "perfis": pd.read_json(CONHECIMENTO_DIR / "perfil_investidor.json"),
        "produtos": pd.read_json(CONHECIMENTO_DIR / "produtos_financeiros.json"),
        "faq": pd.read_json(CONHECIMENTO_DIR / "perguntas_frequentes.json"),
        "transacoes": pd.read_csv(USUARIO_DIR / "transacoes.csv"),
        "historico": pd.read_csv(USUARIO_DIR / "historico_atendimento.csv"),
        "metas": pd.read_json(USUARIO_DIR / "metas_financeiras.json"),
    }
