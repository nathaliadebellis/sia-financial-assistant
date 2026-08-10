import streamlit as st

from finance import obter_maiores_categorias, metas_em_risco, calcular_receitas, calcular_despesas, calcular_saldo
from assistant import processar_pergunta


def renderizar_interface(transacoes, historico, metas, contexto):
    st.title("💰 SIA - Smart Interactive Assistant")

    st.markdown(
        "Esta é a visão inicial da SIA. Aqui você encontra seu resumo financeiro, alertas de metas, gráfico de gastos, resumo detalhado e o chat interativo."
    )

    receitas_atuais = calcular_receitas(transacoes)
    despesas_atuais = calcular_despesas(transacoes)
    saldo_atual = calcular_saldo(transacoes)
    maiores_categorias = obter_maiores_categorias(transacoes, 3)
    metas_risco = metas_em_risco(transacoes, metas)

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Receitas", f"R$ {receitas_atuais:.2f}")
    col2.metric("💸 Despesas", f"R$ {despesas_atuais:.2f}")
    col3.metric("📈 Saldo", f"R$ {saldo_atual:.2f}")

    st.markdown("---")

    st.subheader("⚠️ Alertas de metas")
    if metas_risco:
        for meta in metas_risco:
            st.warning(
                f"{meta['nome']}: {meta['percentual']:.0f}% do orçamento (R$ {meta['valor_atual']:.2f} / R$ {meta['valor_meta']:.2f})"
            )
    else:
        st.success("Nenhuma meta de orçamento está próxima do limite no momento.")

    st.markdown("---")

    st.subheader("📊 Gráfico de gastos")
    despesas_por_categoria = (
        transacoes[
            transacoes["tipo"] == "saida"
        ]
        .assign(categoria=lambda df: df["categoria"].fillna("Sem categoria"))
        .groupby("categoria", dropna=False)["valor"]
        .sum()
        .sort_values(ascending=False)
    )

    if not despesas_por_categoria.empty:
        st.bar_chart(despesas_por_categoria)
    else:
        st.info("Não há despesas registradas para exibir o gráfico.")

    st.markdown("---")

    st.subheader("📋 Resumo detalhado")
    with st.expander("Ver resumo completo"):
        st.write(f"- Total de transações: {len(transacoes)}")
        st.write(f"- Total de entradas: {len(transacoes[transacoes['tipo'] == 'entrada'])}")
        st.write(f"- Total de saídas: {len(transacoes[transacoes['tipo'] == 'saida'])}")
        st.write(f"- Saldo atual: R$ {saldo_atual:.2f}")
        st.write("- Maiores categorias de gasto:")
        if maiores_categorias:
            for categoria, valor in maiores_categorias:
                st.write(f"  - {categoria}: R$ {valor:.2f}")
        else:
            st.write("  - Nenhuma categoria registrada.")
        st.write(f"- Metas em risco: {len(metas_risco)}")

    st.markdown("---")

    st.subheader("💬 Chat da SIA")
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    for mensagem in st.session_state.mensagens:
        with st.chat_message(mensagem["role"]):
            st.write(mensagem["content"])

    pergunta = st.chat_input("Digite sua pergunta:")

    if pergunta:
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.write(pergunta)
        with st.chat_message("assistant"):
            with st.spinner("SIA está pensando..."):
                resposta = processar_pergunta(pergunta, transacoes, historico, metas, contexto)
                st.write(resposta)
        st.session_state.mensagens.append({"role": "assistant", "content": resposta})
