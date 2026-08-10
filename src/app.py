import pandas as pd
import requests
import streamlit as st

# ==================================================
# CONFIGURAÇÕES
# ==================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2:1b"

# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.set_page_config(
    page_title="SIA - Smart Interactive Assistant",
    page_icon="💰",
    layout="centered"
)

# ==================================================
# CARREGAMENTO DOS DADOS
# ==================================================

@st.cache_data
def carregar_dados():

    conceitos = pd.read_json(
        "data/conhecimento/conceitos_financeiros.json"
    )

    perfis = pd.read_json(
        "data/conhecimento/perfil_investidor.json"
    )

    produtos = pd.read_json(
        "data/conhecimento/produtos_financeiros.json"
    )

    faq = pd.read_json(
        "data/conhecimento/perguntas_frequentes.json"
    )

    transacoes = pd.read_csv(
        "data/usuario/transacoes.csv"
    )

    historico = pd.read_csv(
        "data/usuario/historico_atendimento.csv"
    )

    metas = pd.read_json(
        "data/usuario/metas_financeiras.json"
    )

    return (
        conceitos,
        perfis,
        produtos,
        faq,
        transacoes,
        historico,
        metas
    )

(
    conceitos,
    perfis,
    produtos,
    faq,
    transacoes,
    historico,
    metas
) = carregar_dados()

# ==================================================
# PERFIL DO CLIENTE
# ==================================================

perfil = perfis.iloc[0]

# ==================================================
# FUNÇÕES FINANCEIRAS
# ==================================================

def calcular_receitas():

    return transacoes[
        transacoes["tipo"] == "entrada"
    ]["valor"].sum()


def calcular_despesas():

    return transacoes[
        transacoes["tipo"] == "saida"
    ]["valor"].sum()


def calcular_saldo():

    return calcular_receitas() - calcular_despesas()


def gastos_por_categoria(categoria):

    gastos = transacoes[
        transacoes["categoria"].str.lower()
        == categoria.lower()
    ]

    return gastos["valor"].sum()


def gerar_resumo_financeiro():

    receitas = calcular_receitas()
    despesas = calcular_despesas()
    saldo = calcular_saldo()

    return f"""
Resumo financeiro atual:

• Receitas: R$ {receitas:.2f}
• Despesas: R$ {despesas:.2f}
• Saldo: R$ {saldo:.2f}

Sugestão prática: revise categorias como moradia, alimentação e transporte para reduzir gastos.
"""

# ==================================================
# METAS FINANCEIRAS
# ==================================================
def analisar_metas():

    resultado = []

    for _, meta in metas.iterrows():

        valor_meta = float(meta.get("valor_meta", 0) or 0)
        valor_atual = float(meta.get("valor_atual", 0) or 0)
        tipo_meta = str(meta.get("tipo", "")).lower()
        categoria = str(meta.get("categoria", "")).lower()

        if tipo_meta == "orcamento":
            valor_atual = gastos_por_categoria(categoria)

        percentual = (
            (valor_atual / valor_meta) * 100
            if valor_meta > 0 else 0
        )

        resultado.append({
            "nome": meta.get("nome", "Meta"),
            "tipo": tipo_meta,
            "categoria": categoria,
            "valor_meta": valor_meta,
            "valor_atual": valor_atual,
            "percentual": percentual,
            "status": meta.get("status", "n/a"),
            "descricao": meta.get("descricao", "")
        })

    return resultado

def gerar_relatorio_metas():

    metas_analisadas = analisar_metas()

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


def gerar_insights_financeiros():

    despesas = transacoes[
        transacoes["tipo"] == "saida"
    ]

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

def gerar_recomendacoes_acao():

    total_receitas = calcular_receitas()
    total_despesas = calcular_despesas()
    saldo = calcular_saldo()
    despesas = transacoes[
        transacoes["tipo"] == "saida"
    ]

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
            percentual = (valor / total_despesas) * 100
            texto += f"• {categoria}: R$ {valor:.2f} ({percentual:.0f}%)\n"

        texto += "\n"

    metas_criticas = []
    for _, meta in metas.iterrows():
        tipo_meta = str(meta.get("tipo", "")).lower()
        categoria = str(meta.get("categoria", "")).lower()
        valor_meta = float(meta.get("valor_meta", 0) or 0)
        valor_atual = float(meta.get("valor_atual", 0) or 0)

        if tipo_meta == "orcamento":
            valor_atual = gastos_por_categoria(categoria)

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

def gerar_resumo_historico_atendimento():

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


def apresentar_assistente():

    return (
        "Olá! Eu sou a SIA, sua assistente financeira. "
        "Vou usar seus dados de transações, metas e histórico para ajudar você a entender e resolver problemas financeiros. "
        "Pergunte, por exemplo, 'Quanto gastei?', 'Como está meu saldo?' ou 'Como posso reduzir meus gastos?'."
    )


def gerar_resumo_gastos():

    receitas = calcular_receitas()
    despesas = calcular_despesas()
    saldo = calcular_saldo()

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
        transacoes[
            transacoes["tipo"] == "saida"
        ]
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


def obter_maiores_categorias(n=3):

    despesas = transacoes[
        transacoes["tipo"] == "saida"
    ]

    if despesas.empty:
        return []

    categorias = (
        despesas
        .assign(categoria=despesas["categoria"].fillna("Sem categoria"))
        .groupby("categoria", dropna=False)["valor"]
        .sum()
        .sort_values(ascending=False)
    )

    return [
        (categoria, float(valor))
        for categoria, valor in categorias.head(n).items()
    ]


def metas_em_risco():

    riscos = []

    for _, meta in metas.iterrows():
        tipo_meta = str(meta.get("tipo", "")).lower()
        categoria = str(meta.get("categoria", "")).lower()
        valor_meta = float(meta.get("valor_meta", 0) or 0)
        valor_atual = float(meta.get("valor_atual", 0) or 0)

        if tipo_meta == "orcamento":
            valor_atual = gastos_por_categoria(categoria)

        if valor_meta > 0:
            percentual = (valor_atual / valor_meta) * 100
        else:
            percentual = 0

        if percentual >= 80:
            riscos.append({
                "nome": meta.get("nome", "Meta"),
                "percentual": percentual,
                "valor_meta": valor_meta,
                "valor_atual": valor_atual,
            })

    return riscos


# CONTEXTO

contexto = f"""
PERFIL DE INVESTIDOR

Nome:
{perfil['nome']}

Descrição:
{perfil['descricao']}

Características:
{', '.join(perfil['caracteristicas'])}

Objetivos:
{', '.join(perfil['objetivos_comuns'])}

Investimentos adequados:
{', '.join(perfil['investimentos_adequados'])}

CONCEITOS FINANCEIROS

{conceitos.to_json(
    orient='records',
    force_ascii=False,
    indent=2
)}

PRODUTOS FINANCEIROS

{produtos.to_json(
    orient='records',
    force_ascii=False,
    indent=2
)}

PERGUNTAS FREQUENTES

{faq.to_json(
    orient='records',
    force_ascii=False,
    indent=2
)}
"""

# PROMPT DO SISTEMA

SYSTEM_PROMPT = """
Você é a SIA (Smart Interactive Assistant), uma assistente virtual especializada em educação financeira e organização das finanças pessoais.

Seu principal objetivo é ajudar usuários a compreender conceitos financeiros, controlar gastos, planejar objetivos financeiros e desenvolver hábitos financeiros mais conscientes por meio de informações claras, confiáveis e educativas.

Você possui acesso a uma base de conhecimento composta por:

- Conceitos financeiros;
- Perfis de investidor;
- Produtos financeiros;
- Perguntas frequentes;
- Dados financeiros de exemplo.

Utilize essas informações como principal fonte para responder às perguntas do usuário.

REGRAS DE NEGÓCIO

1. Responda prioritariamente utilizando as informações presentes na base de conhecimento fornecida.
2. Nunca invente informações ou apresente dados sem fundamento.
3. Caso a informação solicitada não esteja disponível, informe essa limitação de forma clara e educada.
4. Não faça recomendações personalizadas de investimento.
5. Considere o perfil do investidor quando essa informação estiver disponível e for relevante para a pergunta.
6. Explique conceitos financeiros utilizando linguagem simples, clara e acessível.
7. Utilize exemplos práticos sempre que eles ajudarem na compreensão.
8. Não forneça aconselhamento financeiro, jurídico, tributário ou contábil profissional.
9. Caso a pergunta esteja fora do escopo de educação financeira e organização financeira pessoal, informe educadamente sua especialidade.
10. Utilize apenas as informações disponíveis no contexto recebido.
11. Se o usuário pedir ajuda para resolver um problema financeiro, sugira um plano de ação com passos claros.
12. Ajude a transformar dados em ações práticas, como revisar categorias de gasto e reajustar metas.

ESTILO DE COMUNICAÇÃO

- Seja amigável, acolhedora e profissional.
- Converse de forma natural, como uma assistente virtual ajudando uma pessoa.
- Evite linguagem excessivamente formal ou burocrática.
- Evite responder como um relatório técnico.
- Seja objetiva em perguntas simples.
- Responda primeiro à pergunta e depois complemente com informações úteis quando fizer sentido.
- Evite textos longos quando o usuário fizer perguntas diretas.
- Evite repetir informações desnecessárias.
- Utilize linguagem clara e fácil de entender.
- Demonstre interesse genuíno em ajudar o usuário.

QUANDO FALAR SOBRE GASTOS OU TRANSAÇÕES

- Apresente os valores de forma clara e organizada.
- Responda primeiro com a informação solicitada.
- Sempre que possível, ajude o usuário a interpretar os números.
- Não invente cálculos.
- Utilize apenas os valores presentes no contexto.
- Caso os dados não sejam suficientes para responder com precisão, informe essa limitação.

EXEMPLOS DE COMPORTAMENTO

Pergunta:
"Quanto gastei com alimentação?"

Resposta esperada:
"Você gastou R$ 570,00 com alimentação no período registrado.

A maior parte desse valor veio das compras em supermercado (R$ 450,00), seguida pelos gastos em restaurantes (R$ 120,00).

Se desejar, também posso mostrar quanto a alimentação representa em relação ao total das suas despesas."

Pergunta:
"O que é Tesouro Selic?"

Resposta esperada:
"O Tesouro Selic é um título público federal cuja rentabilidade acompanha a taxa Selic, a taxa básica de juros da economia brasileira.

Ele costuma ser utilizado por investidores que buscam segurança, liquidez e formação de reserva de emergência."

IMPORTANTE

- Baseie suas respostas apenas nas informações disponíveis no contexto recebido.
- Quando houver dúvida ou informação insuficiente, peça esclarecimentos ao usuário.
- Mantenha sempre um tom educativo, respeitoso e prestativo."""


# ==================================================
# CONSULTA AO OLLAMA
# ==================================================

def perguntar(pergunta_usuario):

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO:

{contexto}

PERGUNTA:

{pergunta_usuario}
"""

    try:

        resposta = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        resposta.raise_for_status()

        dados = resposta.json()

        if "error" in dados:
            return f"Erro do Ollama: {dados['error']}"

        if "response" in dados:
            return dados["response"]

        return f"Resposta inesperada: {dados}"

    except requests.exceptions.Timeout:
        return (
            "O modelo demorou muito para responder. "
            "Tente utilizar um modelo menor."
        )

    except requests.exceptions.ConnectionError:
        return (
            "Não foi possível conectar ao Ollama. "
            "Verifique se ele está em execução."
        )

    except Exception as erro:
        return f"Erro: {erro}"


# ==================================================
# PROCESSAMENTO DAS PERGUNTAS
# ==================================================

def eh_saudacao(texto):

    saudacoes = (
        "olá",
        "ola",
        "oi",
        "bom dia",
        "boa tarde",
        "boa noite",
    )

    texto = texto.strip()

    if texto in saudacoes:
        return True

    if texto.endswith(("?", "!", ".")):
        texto_sem_pont = texto[:-1].strip()
        return texto_sem_pont in saudacoes

    return False


def remover_saudacao_inicial(texto):

    saudacoes = (
        "olá",
        "ola",
        "oi",
        "bom dia",
        "boa tarde",
        "boa noite",
    )

    texto = texto.strip()

    for saudacao in saudacoes:
        prefixos = (
            saudacao + " ",
            saudacao + ",",
            saudacao + "!",
            saudacao + ".",
        )

        for prefixo in prefixos:
            if texto.startswith(prefixo):
                return texto[len(prefixo):].strip(" ,!?.")

    return texto


def processar_pergunta(pergunta):

    texto = pergunta.lower().strip()

    # Saudação

    if eh_saudacao(texto):
        return apresentar_assistente()

    texto = remover_saudacao_inicial(texto)

    # Metas

    if (
        "meta" in texto
        or "metas" in texto
        or "orçamento" in texto
        or "orcamento" in texto
    ):
        return gerar_relatorio_metas()

    # Resumo financeiro

    if (
        "situação financeira" in texto
        or "resumo financeiro" in texto
        or "como estão minhas finanças" in texto
        or "meu saldo" in texto
        or "saldo" in texto
        or "estado financeiro" in texto
    ):
        return gerar_resumo_financeiro()

    # Alimentação

    if (
        "alimentação" in texto
        or "alimentacao" in texto
    ):

        total = gastos_por_categoria(
            "alimentacao"
        )

        return f"""
Você gastou R$ {total:.2f} com alimentação no período analisado.

Esse valor considera os gastos registrados em supermercado e restaurantes.

Se desejar, também posso detalhar essas despesas.
"""

    # Transporte

    if "transporte" in texto:

        total = gastos_por_categoria(
            "transporte"
        )

        return f"""
Você gastou R$ {total:.2f} com transporte no período analisado.

Essa categoria inclui gastos como Uber e combustível registrados nas transações.
"""

    # Moradia

    if "moradia" in texto:

        total = gastos_por_categoria(
            "moradia"
        )

        return f"""
Você gastou R$ {total:.2f} com moradia no período analisado.
"""

    # Saúde

    if (
        "saúde" in texto
        or "saude" in texto
    ):

        total = gastos_por_categoria(
            "saude"
        )

        return f"""
Você gastou R$ {total:.2f} com saúde no período analisado.
"""

    # Lazer

    if "lazer" in texto:

        total = gastos_por_categoria(
            "lazer"
        )

        return f"""
Você gastou R$ {total:.2f} com lazer no período analisado.
"""

    # Resumo geral de gastos

    if (
        "gasto" in texto
        or "gastos" in texto
        or "despesa" in texto
        or "despesas" in texto
        or "receita" in texto
        or "receitas" in texto
        or "transação" in texto
        or "transacao" in texto
        or "transacoes" in texto
    ):
        return gerar_resumo_gastos()

    # Resolver problema financeiro

    if (
        "resolver" in texto
        or "ajuda" in texto
        or "ajudar" in texto
        or "problema" in texto
        or "reduzir" in texto
        or "cortar" in texto
        or "economizar" in texto
        or "melhorar" in texto
    ):
        return gerar_recomendacoes_acao()

    # Insights financeiros

    if (
        "insight" in texto
        or "análise dos gastos" in texto
        or "analise dos gastos" in texto
        or "como estou gastando" in texto
        or "onde estou gastando" in texto
        or "quais gastos" in texto
    ):
        return gerar_insights_financeiros()

    # Histórico de atendimento

    if (
        "histórico" in texto
        or "historico" in texto
        or "atendimento" in texto
        or "interações" in texto
        or "interacoes" in texto
        or "cliente" in texto
        or "suporte" in texto
    ):
        return gerar_resumo_historico_atendimento()

    # Perguntas gerais

    return perguntar(pergunta)


# ==================================================
# INTERFACE
# ==================================================

st.title("💰 SIA - Smart Interactive Assistant")

st.markdown("### Resumo financeiro")

receitas_atuais = calcular_receitas()
despesas_atuais = calcular_despesas()
saldo_atual = calcular_saldo()
maiores_categorias = obter_maiores_categorias(3)
metas_risco = metas_em_risco()

col1, col2, col3 = st.columns(3)
col1.metric("Receitas", f"R$ {receitas_atuais:.2f}")
col2.metric("Despesas", f"R$ {despesas_atuais:.2f}")
col3.metric("Saldo", f"R$ {saldo_atual:.2f}")

with st.expander("Detalhes do resumo"):
    if maiores_categorias:
        st.write("**Maiores categorias de gasto:**")
        for categoria, valor in maiores_categorias:
            st.write(f"- {categoria}: R$ {valor:.2f}")
    else:
        st.write("Não há despesas registradas para mostrar categorias.")

    if metas_risco:
        st.write("**Metas em risco:**")
        for meta in metas_risco:
            st.write(
                f"- {meta['nome']}: {meta['percentual']:.0f}% do orçamento (R$ {meta['valor_atual']:.2f} / R$ {meta['valor_meta']:.2f})"
            )
    else:
        st.write("Nenhuma meta de orçamento está próxima do limite no momento.")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for mensagem in st.session_state.mensagens:

    with st.chat_message(
        mensagem["role"]
    ):
        st.write(
            mensagem["content"]
        )

pergunta = st.chat_input(
    "Digite sua pergunta:"
)

if pergunta:

    st.session_state.mensagens.append({
        "role": "user",
        "content": pergunta
    })

    with st.chat_message("user"):
        st.write(pergunta)

    with st.chat_message("assistant"):

        with st.spinner(
            "SIA está pensando..."
        ):

            resposta = processar_pergunta(
                pergunta
            )

            st.write(resposta)

    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resposta
    })