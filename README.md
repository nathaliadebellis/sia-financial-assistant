# 💰 SIA - Smart Interactive Assistant

A SIA (Smart Interactive Assistant) é uma assistente virtual desenvolvida para apoiar usuários na educação financeira e na organização das finanças pessoais por meio de uma experiência conversacional baseada em Inteligência Artificial.

O projeto combina conceitos de IA Generativa, manipulação de dados e desenvolvimento de aplicações em Python para oferecer uma interface interativa de perguntas e respostas financeiras.

---

# 📌 Objetivo

A SIA tem como objetivo transformar dados financeiros em conhecimento acessível, ajudando o usuário a compreender conceitos financeiros, analisar gastos e tomar decisões mais conscientes.

A aplicação foi projetada para:

- Explicar conceitos financeiros de forma simples e objetiva;
- Consultar informações de uma base de conhecimento estruturada;
- Interpretar dados financeiros de exemplo;
- Auxiliar no acompanhamento de receitas, despesas e metas;
- Incentivar hábitos financeiros mais saudáveis;
- Demonstrar aplicação prática de IA Generativa em um ambiente local.

---

# 🚀 Tecnologias Utilizadas

## Linguagem e Framework

- Python
- Streamlit

## Manipulação de Dados

- Pandas

## Inteligência Artificial

- Ollama
- LLM local: `llama3.2:1b`

## Consumo de APIs

- Requests

## Estruturação de Dados

- JSON
- CSV

## Controle de Versão

- Git
- GitHub

---

# 🧠 Como o modelo funciona

A SIA utiliza um modelo de linguagem local rodando no Ollama para gerar respostas quando a pergunta não se encaixa em regras específicas de intenção.

O aplicativo tenta processar perguntas diretamente com lógica local para evitar respostas genéricas e só consulta o modelo quando necessário.

O endpoint utilizado é:

```python
http://localhost:11434/api/generate
```

---

# 📂 Estrutura do Projeto

```text
sia-financial-assistent
│
├── data/
│   ├── conhecimento/
│   │   ├── conceitos_financeiros.json
│   │   ├── perfil_investidor.json
│   │   ├── produtos_financeiros.json
│   │   ├── perguntas_frequentes.json
│   └── usuario/
│       ├── transacoes.csv
│       ├── historico_atendimento.csv
│       └── metas_financeiras.json
│
├── docs/
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   └── 03-prompts.md
│   
│
├── src/
│   ├── app.py
│   ├── assistant.py
│   ├── data_loader.py
│   ├── finance.py
│   └── ui.py
│   
│
├── requirements.txt
└── README.md
```

---

# 📚 Base de Conhecimento e Dados

A SIA utiliza arquivos JSON como base de conhecimento e arquivos CSV/JSON como dados de usuário.

- `data/conhecimento/` contém conceitos, perfis de investidor, produtos financeiros e perguntas frequentes.
- `data/usuario/` contém transações, histórico de atendimento e metas financeiras.

Essa separação permite atualizar o conteúdo educativo independentemente dos exemplos financeiros do usuário.

---

# 💬 Funcionalidades

### Educação Financeira

A SIA responde dúvidas sobre:

- conceitos financeiros;
- perfil de investidor;
- produtos financeiros;
- perguntas frequentes.

### Análise de Dados Financeiros

A SIA também analisa dados locais para fornecer:

- resumo de receitas, despesas e saldo;
- alertas de metas em risco;
- gráfico de gastos por categoria;
- insights financeiros baseados nas transações.

### Atendimento Conversacional

A interface oferece um chat interativo em que o usuário pode digitar perguntas e receber respostas da assistente.

Exemplos de perguntas:

```text
Quanto gastei com alimentação?
Qual meu saldo atual?
Como está minha situação financeira?
O que é reserva de emergência?
```

---

# 🧩 Arquitetura de Código

O código atual está distribuído em módulos:

- `src/app.py`: ponto de entrada do Streamlit e montagem do contexto;
- `src/ui.py`: renderiza o dashboard e o chat;
- `src/assistant.py`: identifica intenções e faz a chamada ao modelo quando necessário;
- `src/finance.py`: contém funções de cálculo financeiro e geração de relatórios;
- `src/data_loader.py`: carrega os dados de `data/` em memória.

---

# ⚙️ Como Executar

## 1. Clonar o repositório

```bash
git clone https://github.com/nathaliadebellis/sia-financial-assistant.git
```

## 2. Acessar a pasta do projeto

```bash
cd sia-financial-assistant
```

## 3. Criar ambiente virtual

```bash
python -m venv .venv
```

## 4. Ativar ambiente virtual

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/Mac:

```bash
source .venv/bin/activate
```

## 5. Instalar dependências

```bash
pip install -r requirements.txt
```

## 6. Instalar o Ollama

Baixe e instale o Ollama em https://ollama.com

Em seguida, baixe o modelo local:

```bash
ollama pull llama3.2:1b
```

## 7. Executar o aplicativo

```bash
streamlit run src/app.py
```

---

# 🎓 Aprendizados Aplicados

Este projeto demonstra aplicação prática de:

- IA Generativa com modelo local;
- Engenharia de prompt e contexto;
- Estruturação de base de conhecimento;
- Manipulação e análise de dados com Pandas;
- Interface web com Streamlit;
- Modularização de código em Python;
- Documentação do projeto.


```bash
streamlit run src/app.py
```

---

# 🎓 Aprendizados Aplicados

Este projeto foi desenvolvido como exercício prático de aplicação dos conhecimentos adquiridos durante o **Bootcamp Bradesco - GenAI, Dados & Cyber**, envolvendo:

- Inteligência Artificial Generativa;
- Engenharia de Prompt;
- Estruturação de bases de conhecimento;
- Manipulação e análise de dados;
- Desenvolvimento de aplicações em Python;
- Integração com APIs;
- Construção de interfaces web com Streamlit;
- Organização e documentação de projetos.

---

