import streamlit as st

from data_loader import carregar_dados
from ui import renderizar_interface

# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.set_page_config(
    page_title="SIA - Smart Interactive Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
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

    st.sidebar.markdown(
        "<div class='sidebar-card'>"
        "<div class='sidebar-title'>Modo Demo</div>"
        "<div class='sidebar-description'>Ative para exibir um painel de demonstração com visual pronto para screenshots.</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    modo_demo = st.sidebar.checkbox("Ativar modo demo", value=True)
    st.sidebar.markdown(
        "<div class='sidebar-card'>"
        "<div class='sidebar-title'>Sobre a SIA</div>"
        "<div class='sidebar-description'>Assistente financeira baseada em IA para educação financeira e organização das finanças pessoais.</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    renderizar_interface(
        dados["transacoes"],
        dados["historico"],
        dados["metas"],
        contexto,
        modo_demo=modo_demo,
    )


if __name__ == "__main__":
    main()
