from typing import Dict, List, Tuple


def calcular_receitas(transacoes):
    return transacoes[transacoes["tipo"] == "entrada"]["valor"].sum()


def calcular_despesas(transacoes):
    return transacoes[transacoes["tipo"] == "saida"]["valor"].sum()


def calcular_saldo(transacoes):
    return calcular_receitas(transacoes) - calcular_despesas(transacoes)


def gastos_por_categoria(transacoes, categoria: str):
    gastos = transacoes[transacoes["categoria"].str.lower() == categoria.lower()]
    return gastos["valor"].sum()


def gerar_resumo_financeiro(transacoes):
    receitas = calcular_receitas(transacoes)
    despesas = calcular_despesas(transacoes)
    saldo = calcular_saldo(transacoes)

    return (
        f"Resumo financeiro atual:\n\n"
        f"• Receitas: R$ {receitas:.2f}\n"
        f"• Despesas: R$ {despesas:.2f}\n"
        f"• Saldo: R$ {saldo:.2f}\n\n"
        "Sugestão prática: revise categorias como moradia, alimentação e transporte para reduzir gastos."
    )


def analisar_metas(transacoes, metas):
    resultado = []

    for _, meta in metas.iterrows():
        valor_meta = float(meta.get("valor_meta", 0) or 0)
        valor_atual = float(meta.get("valor_atual", 0) or 0)
        tipo_meta = str(meta.get("tipo", "")).lower()
        categoria = str(meta.get("categoria", "")).lower()

        if tipo_meta == "orcamento":
            valor_atual = gastos_por_categoria(transacoes, categoria)

        percentual = (valor_atual / valor_meta) * 100 if valor_meta > 0 else 0

        resultado.append({
            "nome": meta.get("nome", "Meta"),
            "tipo": tipo_meta,
            "categoria": categoria,
            "valor_meta": valor_meta,
            "valor_atual": valor_atual,
            "percentual": percentual,
            "status": meta.get("status", "n/a"),
            "descricao": meta.get("descricao", ""),
        })

    return resultado


def gerar_relatorio_metas(transacoes, metas):
    metas_analisadas = analisar_metas(transacoes, metas)

    if not metas_analisadas:
        return (
            "Ainda não há metas cadastradas. "
            "Adicione metas financeiras para acompanhar seu progresso."
        )

    texto = "📊 Metas Financeiras\n\n"

    for meta in metas_analisadas:
        texto += (
            f"• {meta['nome']}\n"
            f"Tipo: {meta['tipo'].capitalize()}\n"
            f"Meta: R$ {meta['valor_meta']:.2f}\n"
            f"Atual: R$ {meta['valor_atual']:.2f}\n"
            f"Progresso: {meta['percentual']:.0f}%\n"
            f"Status: {meta['status']}\n"
        )

        if meta['tipo'] == "orcamento":
            texto += "Resumo: mostra o quanto você já gastou na categoria definida.\n\n"
        else:
            texto += "Resumo: mostra o avanço em direção à meta financeira.\n\n"

    return texto


def gerar_insights_financeiros(transacoes):
    despesas = transacoes[transacoes["tipo"] == "saida"]

    if despesas.empty:
        return (
            "Não há despesas registradas no período analisado. "
            "Assim, não consigo gerar insights financeiros detalhados."
        )

    total_despesas = despesas["valor"].sum()
    categorias = (
        despesas
        .assign(categoria=despesas["categoria"].fillna("Sem categoria"))
        .groupby("categoria", dropna=False)["valor"]
        .sum()
        .sort_values(ascending=False)
    )

    maior_categoria = categorias.index[0]
    maior_valor = categorias.iloc[0]
    porcentagem = (maior_valor / total_despesas) * 100

    texto = (
        "Aqui estão alguns insights financeiros com base nas despesas registradas:\n\n"
        f"• Total de despesas: R$ {total_despesas:.2f}\n"
        f"• Categoria com maior gasto: {maior_categoria} (R$ {maior_valor:.2f}, {porcentagem:.0f}% do total)\n\n"
    )

    texto += "Distribuição de despesas por categoria:\n"

    for categoria, valor in categorias.items():
        percentual = (valor / total_despesas) * 100
        texto += f"• {categoria}: R$ {valor:.2f} ({percentual:.0f}%)\n"

    return texto


def gerar_recomendacoes_acao(transacoes, metas):
    total_receitas = calcular_receitas(transacoes)
    total_despesas = calcular_despesas(transacoes)
    saldo = calcular_saldo(transacoes)
    despesas = transacoes[transacoes["tipo"] == "saida"]

    if total_receitas == 0:
        return (
            "Não há receitas registradas no período analisado. "
            "Para começar a resolver o problema, verifique se todas as entradas foram registradas corretamente."
        )

    texto = "📌 Plano de ação financeiro:\n\n"

    if saldo < 0:
        texto += (
            "Seu saldo está negativo, o que indica que as despesas superam as receitas. "
            "Isso é o principal problema a ser resolvido no momento.\n\n"
        )
    elif saldo < total_receitas * 0.15:
        texto += (
            "Seu saldo está positivo, mas ainda é muito apertado. "
            "Vale priorizar a redução dos maiores gastos para ganhar margem de segurança.\n\n"
        )
    else:
        texto += (
            "Seu saldo está positivo. "
            "Agora o foco pode ser organizar metas e garantir que as despesas não cresçam demais.\n\n"
        )

    categorias = (
        despesas
        .assign(categoria=despesas["categoria"].fillna("Sem categoria"))
        .groupby("categoria", dropna=False)["valor"]
        .sum()
        .sort_values(ascending=False)
    )

    if not categorias.empty:
        texto += "Principais categorias de gasto:\n"
        for categoria, valor in categorias.head(3).items():
            percentual = (valor / total_despesas) * 100 if total_despesas > 0 else 0
            texto += f"• {categoria}: R$ {valor:.2f} ({percentual:.0f}%)\n"

        texto += "\n"

    metas_criticas = []
    for _, meta in metas.iterrows():
        tipo_meta = str(meta.get("tipo", "")).lower()
        categoria = str(meta.get("categoria", "")).lower()
        valor_meta = float(meta.get("valor_meta", 0) or 0)
        valor_atual = float(meta.get("valor_atual", 0) or 0)

        if tipo_meta == "orcamento":
            valor_atual = gastos_por_categoria(transacoes, categoria)

        if valor_meta > 0 and valor_atual >= valor_meta * 0.8:
            metas_criticas.append((meta.get("nome", "Meta"), valor_atual, valor_meta))

    if metas_criticas:
        texto += "Metas de orçamento próximas do limite:\n"
        for nome, atual, meta_valor in metas_criticas:
            texto += (
                f"• {nome}: R$ {atual:.2f} / R$ {meta_valor:.2f} "
                f"({(atual / meta_valor) * 100:.0f}%)\n"
            )
        texto += "\n"

    texto += (
        "Sugestões imediatas:\n"
        "1. Reduza os maiores gastos fixos ou recorrentes.\n"
        "2. Reveja metas de orçamento que já estão no limite.\n"
        "3. Monitore despesas semanais para evitar surpresas no fim do mês.\n"
    )

    if saldo < 0:
        texto += (
            "\nPriorize ações como cortar gastos não essenciais, renegociar serviços e aumentar a reserva de emergência."
        )
    else:
        texto += (
            "\nSe quiser, posso ajudar a montar um plano de economia por categoria."
        )

    return texto


def gerar_resumo_historico_atendimento(transacoes, historico):
    if historico.empty:
        return (
            "Ainda não há registros de histórico de atendimento. "
            "Quando houver interações, eu poderei resumir os principais temas e canais."
        )

    total_atendimentos = len(historico)
    atendimentos_resolvidos = historico[
        historico["resolvido"].astype(str).str.lower() == "sim"
    ]
    percentual_resolvido = (
        (len(atendimentos_resolvidos) / total_atendimentos) * 100
        if total_atendimentos > 0 else 0
    )

    canais = historico["canal"].value_counts()
    canal_mais_usado = canais.index[0] if not canais.empty else "não disponível"

    temas = historico["tema"].value_counts().head(3)
    top_temas = "\n".join(
        f"• {tema}: {contagem} vez(es)"
        for tema, contagem in temas.items()
    )

    texto = (
        "📌 Resumo do Histórico de Atendimento\n\n"
        f"Total de interações registradas: {total_atendimentos}\n"
        f"Canal mais usado: {canal_mais_usado}\n"
        f"Taxa de resolução: {percentual_resolvido:.0f}%\n\n"
        "Principais temas abordados:\n"
        f"{top_temas}\n"
    )

    return texto


def gerar_resumo_gastos(transacoes):
    receitas = calcular_receitas(transacoes)
    despesas = calcular_despesas(transacoes)
    saldo = calcular_saldo(transacoes)

    if receitas == 0 and despesas == 0:
        return (
            "Ainda não há transações registradas no período analisado. "
            "Quando você tiver dados, posso analisar seus gastos e sugerir melhorias."
        )

    texto = (
        "Aqui está um resumo do seu fluxo financeiro registrado:\n\n"
        f"• Receitas: R$ {receitas:.2f}\n"
        f"• Despesas: R$ {despesas:.2f}\n"
        f"• Saldo: R$ {saldo:.2f}\n\n"
    )

    if saldo < 0:
        texto += (
            "Seu saldo está negativo, o que indica que suas despesas estão maiores que suas receitas. "
            "Para resolver isso, podemos focar em reduzir gastos e priorizar despesas essenciais.\n"
        )
    elif saldo < receitas * 0.15:
        texto += (
            "Seu saldo está positivo, mas ainda apertado. "
            "Vale a pena reduzir despesas variáveis e reforçar o controle dos orçamentos.\n"
        )
    else:
        texto += (
            "Seu saldo está confortável. "
            "Agora o foco pode ser manter o controle e avançar nas metas financeiras.\n"
        )

    categorias = (
        transacoes[transacoes["tipo"] == "saida"]
        .assign(categoria=transacoes["categoria"].fillna("Sem categoria"))
        .groupby("categoria", dropna=False)["valor"]
        .sum()
        .sort_values(ascending=False)
    )

    if not categorias.empty:
        texto += "\nPrincipais categorias de gasto:\n"
        for categoria, valor in categorias.head(3).items():
            percentual = (valor / despesas) * 100 if despesas > 0 else 0
            texto += f"• {categoria}: R$ {valor:.2f} ({percentual:.0f}%)\n"

        texto += "\n"

        if categorias.iloc[0] >= despesas * 0.3:
            texto += (
                f"A categoria '{categorias.index[0]}' concentra {categorias.iloc[0] / despesas * 100:.0f}% das despesas. "
                "Esse é um bom ponto de partida para reduzir gastos."
            )
        else:
            texto += (
                "Se desejar, posso sugerir cortes nas categorias com os maiores valores."
            )
    else:
        texto += "Posso detalhar suas despesas por categoria ou sugerir ações práticas para melhorar seu resultado."

    return texto


def obter_maiores_categorias(transacoes, n=3):
    despesas = transacoes[transacoes["tipo"] == "saida"]

    if despesas.empty:
        return []

    categorias = (
        despesas
        .assign(categoria=despesas["categoria"].fillna("Sem categoria"))
        .groupby("categoria", dropna=False)["valor"]
        .sum()
        .sort_values(ascending=False)
    )

    return [(categoria, float(valor)) for categoria, valor in categorias.head(n).items()]


def metas_em_risco(transacoes, metas):
    riscos = []

    for _, meta in metas.iterrows():
        tipo_meta = str(meta.get("tipo", "")).lower()
        categoria = str(meta.get("categoria", "")).lower()
        valor_meta = float(meta.get("valor_meta", 0) or 0)
        valor_atual = float(meta.get("valor_atual", 0) or 0)

        if tipo_meta == "orcamento":
            valor_atual = gastos_por_categoria(transacoes, categoria)

        percentual = (valor_atual / valor_meta) * 100 if valor_meta > 0 else 0

        if percentual >= 80:
            riscos.append({
                "nome": meta.get("nome", "Meta"),
                "percentual": percentual,
                "valor_meta": valor_meta,
                "valor_atual": valor_atual,
            })

    return riscos
