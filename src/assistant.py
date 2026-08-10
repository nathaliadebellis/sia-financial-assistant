import requests

from finance import (
    gerar_insights_financeiros,
    gerar_relatorio_metas,
    gerar_recomendacoes_acao,
    gerar_resumo_financeiro,
    gerar_resumo_gastos,
    gerar_resumo_historico_atendimento,
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2:1b"

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
"""


def perguntar(pergunta_usuario, contexto):
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
                "stream": False,
            },
            timeout=120,
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


def apresentar_assistente():
    return (
        "Olá! Eu sou a SIA, sua assistente financeira. "
        "Vou usar seus dados de transações, metas e histórico para ajudar você a entender e resolver problemas financeiros. "
        "Pergunte, por exemplo, 'Quanto gastei?', 'Como está meu saldo?' ou 'Como posso reduzir meus gastos?'."
    )


def processar_pergunta(pergunta, transacoes, historico, metas, contexto):
    texto = pergunta.lower().strip()
    if eh_saudacao(texto):
        return apresentar_assistente()

    texto = remover_saudacao_inicial(texto)

    if (
        "meta" in texto
        or "metas" in texto
        or "orçamento" in texto
        or "orcamento" in texto
    ):
        return gerar_relatorio_metas(transacoes, metas)

    if (
        "situação financeira" in texto
        or "resumo financeiro" in texto
        or "como estão minhas finanças" in texto
        or "meu saldo" in texto
        or "saldo" in texto
        or "estado financeiro" in texto
    ):
        return gerar_resumo_financeiro(transacoes)

    if (
        "alimentação" in texto
        or "alimentacao" in texto
    ):
        return gerar_resumo_gastos(transacoes)

    if "transporte" in texto:
        return gerar_resumo_gastos(transacoes)

    if "moradia" in texto:
        return gerar_resumo_gastos(transacoes)

    if (
        "saúde" in texto
        or "saude" in texto
    ):
        return gerar_resumo_gastos(transacoes)

    if "lazer" in texto:
        return gerar_resumo_gastos(transacoes)

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
        return gerar_resumo_gastos(transacoes)

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
        return gerar_recomendacoes_acao(transacoes, metas)

    if (
        "insight" in texto
        or "análise dos gastos" in texto
        or "analise dos gastos" in texto
        or "como estou gastando" in texto
        or "onde estou gastando" in texto
        or "quais gastos" in texto
    ):
        return gerar_insights_financeiros(transacoes)

    if (
        "histórico" in texto
        or "historico" in texto
        or "atendimento" in texto
        or "interações" in texto
        or "interacoes" in texto
        or "cliente" in texto
        or "suporte" in texto
    ):
        return gerar_resumo_historico_atendimento(historico)

    return perguntar(pergunta, contexto)
