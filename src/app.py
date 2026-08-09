import pandas as pd

# Carregamento dos arquivos JSON

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

# Carregamento dos arquivos CSV

transacoes = pd.read_csv(
    "data/exemplos/transacoes.csv"
)

historico = pd.read_csv(
    "data/exemplos/historico_atendimento.csv"
)

print("Base de conhecimento carregada com sucesso.")

perfil = perfis.iloc[0]

contexto = f"""
PERFIL DE INVESTIDOR

Nome: {perfil['nome']}

Descrição:
{perfil['descricao']}

Características:
{', '.join(perfil['caracteristicas'])}

Objetivos comuns:
{', '.join(perfil['objetivos_comuns'])}

Investimentos adequados:
{', '.join(perfil['investimentos_adequados'])}

TRANSAÇÕES RECENTES

{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES

{historico.to_string(index=False)}
"""

print(contexto)