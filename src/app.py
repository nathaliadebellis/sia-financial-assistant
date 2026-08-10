import streamlit as st

from data_loader import carregar_dados
from ui import renderizar_interface

# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.set_page_config(
    page_title="SIA - Smart Interactive Assistant",
    page_icon="💰",
    layout="centered",
)


@st.cache_data
def carregar_dados_cache():
    return carregar_dados()


def construir_contexto(conceitos, perfis, produtos, faq):
    perfil = perfis.iloc[0] if not perfis.empty else {}
    nome = perfil.get("nome", "Não disponível")
    descricao = perfil.get("descricao", "Não disponível")
    caracteristicas = ", ".join(perfil.get("caracteristicas", []))
    objetivos = ", ".join(perfil.get("objetivos_comuns", []))
    investimentos = ", ".join(perfil.get("investimentos_adequados", []))

    return f"""
PERFIL DE INVESTIDOR

Nome:
{nome}

Descrição:
{descricao}

Características:
{caracteristicas}

Objetivos:
{objetivos}

Investimentos adequados:
{investimentos}

CONCEITOS FINANCEIROS

{conceitos.to_json(orient='records', force_ascii=False, indent=2)}

PRODUTOS FINANCEIROS

{produtos.to_json(orient='records', force_ascii=False, indent=2)}

PERGUNTAS FREQUENTES

{faq.to_json(orient='records', force_ascii=False, indent=2)}
"""


def main():
    dados = carregar_dados_cache()
    contexto = construir_contexto(
        dados["conceitos"],
        dados["perfis"],
        dados["produtos"],
        dados["faq"],
    )

    renderizar_interface(
        dados["transacoes"],
        dados["historico"],
        dados["metas"],
        contexto,
    )


if __name__ == "__main__":
    main()
