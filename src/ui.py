import html
import pandas as pd
import streamlit as st

from assistant import processar_pergunta
from finance import (
    calcular_despesas,
    calcular_receitas,
    calcular_saldo,
    metas_em_risco,
    obter_maiores_categorias,
)


def aplicar_estilos() -> None:
    st.markdown(
        """
        <style>
            html, body, .stApp, .main, .block-container, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
                background: #F8FAFC !important;
                color: #0F172A !important;
            }

            .block-container {
                padding: 2rem 2.4rem 2.4rem !important;
            }

            section[data-testid="stSidebar"] {
                min-width: 280px !important;
                max-width: 300px !important;
            }

            .stSidebar .stTextInput>div>div>input,
            .stSidebar .stTextInput>div>div>textarea,
            .stSidebar .stSelectbox>div>div>div>div,
            .stSidebar .stCheckbox label {
                border-radius: 16px !important;
                border: 1px solid rgba(15, 118, 110, 0.18) !important;
                background: #FFFFFF !important;
                color: #0F172A !important;
            }

            .stSidebar .stCheckbox label {
                font-weight: 700 !important;
            }

            .stButton>button {
                border-radius: 18px !important;
                border: none !important;
                background-color: #0F766E !important;
                color: #FFFFFF !important;
                padding: 0.9rem 1.35rem !important;
                font-weight: 700 !important;
                box-shadow: 0 14px 28px rgba(15, 118, 110, 0.18) !important;
            }

            .stButton>button:hover,
            .stButton>button:focus {
                background-color: #14B8A6 !important;
            }

            .hero-card,
            .metric-card,
            .summary-card,
            .alert-card,
            .chart-card,
            .chat-card,
            .sidebar-card {
                background: #FFFFFF;
                border-radius: 28px;
                border: 1px solid rgba(15, 118, 110, 0.12);
                box-shadow: 0 22px 60px rgba(15, 23, 42, 0.08);
                color: #0F172A;
            }

            .hero-card {
                padding: 34px 36px;
                border-left: 6px solid #0F766E;
                background: linear-gradient(135deg, #FFFFFF 0%, #ECFEF8 100%);
                margin-bottom: 30px;
            }

            .hero-badge {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 0.55rem 1rem;
                border-radius: 999px;
                background: rgba(15, 118, 110, 0.12);
                color: #0F766E;
                font-size: 0.88rem;
                font-weight: 800;
                letter-spacing: 0.04em;
                margin-bottom: 18px;
            }

            .hero-title {
                font-size: 2.8rem;
                line-height: 1.05;
                font-weight: 900;
                margin-bottom: 18px;
            }

            .hero-subtitle {
                font-size: 1.05rem;
                max-width: 760px;
                color: #475569;
                line-height: 1.75;
            }

            .metrics-row,
            .summary-row,
            .chat-row {
                display: grid;
                gap: 20px;
                margin-bottom: 28px;
            }

            .metrics-row {
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }

            .summary-row {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .metric-card,
            .summary-card,
            .chart-card,
            .chat-card,
            .alert-card {
                padding: 24px;
            }

            .metric-label,
            .summary-title,
            .section-title,
            .chat-title,
            .sidebar-title {
                font-size: 1rem;
                font-weight: 800;
                margin-bottom: 12px;
                color: #0F172A;
            }

            .metric-value {
                font-size: 2rem;
                font-weight: 800;
                margin-bottom: 12px;
                line-height: 1.1;
            }

            .metric-value.receitas { color: #0F766E; }
            .metric-value.despesas { color: #EF4444; }
            .metric-value.saldo { color: #0F766E; }

            .metric-note,
            .summary-text,
            .section-description,
            .chat-intro,
            .chart-note,
            .sidebar-description {
                color: #475569;
                line-height: 1.75;
                font-size: 0.95rem;
            }

            .summary-list {
                padding-left: 1.1rem;
                margin-top: 18px;
                color: #475569;
                font-size: 0.95rem;
                line-height: 1.75;
            }

            .summary-list li {
                margin-bottom: 0.85rem;
            }

            .badge-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.55rem;
                padding: 0.8rem 1rem;
                border-radius: 999px;
                font-size: 0.92rem;
                font-weight: 700;
                margin-top: 16px;
            }

            .badge-pill.primary { background: rgba(15, 118, 110, 0.12); color: #0F766E; }
            .badge-pill.success { background: #ECFDF5; color: #166534; }
            .badge-pill.warning { background: #FEF3C7; color: #B45309; }

            .alert-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.95rem 1.2rem;
                border-radius: 18px;
                font-size: 0.95rem;
                font-weight: 700;
                margin-bottom: 14px;
            }

            .alert-pill.warning { background: #FEF3C7; color: #B45309; }
            .alert-pill.success { background: #ECFDF5; color: #166534; }

            .chart-card { margin-bottom: 30px; }
            .chat-card { margin-bottom: 32px; }
            .chat-title { font-size: 1.05rem; }
            .chat-intro { margin-bottom: 20px; }
            .chat-messages { display: grid; gap: 14px; margin-bottom: 20px; }

            .message-card {
                border-radius: 22px;
                padding: 18px 20px;
                max-width: 100%;
                line-height: 1.75;
                word-break: break-word;
            }

            .message-card.user { background: #0F172A; color: #F8FAFC; margin-left: auto; text-align: right; }
            .message-card.assistant { background: #ECFEF8; color: #0F172A; border: 1px solid rgba(15, 118, 110, 0.18); margin-right: auto; }
            .message-role { font-size: 0.85rem; font-weight: 700; opacity: 0.85; margin-bottom: 8px; }

            .sidebar-card { padding: 22px; margin-bottom: 18px; }
            .sidebar-title { font-size: 1rem; margin-bottom: 10px; }
            .sidebar-description { font-size: 0.96rem; color: #475569; }

            .demo-banner {
                border-radius: 22px;
                background: #0F766E;
                color: #FFFFFF;
                padding: 18px 22px;
                margin-bottom: 24px;
                border: 1px solid rgba(255, 255, 255, 0.22);
            }

            .demo-banner strong { display: block; font-size: 1rem; margin-bottom: 4px; }
            .demo-banner span { color: rgba(255, 255, 255, 0.88); font-size: 0.95rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_hero() -> None:
    st.markdown(
        """
        <div class='hero-card'>
            <div class='hero-badge'>Painel Financeiro Inteligente</div>
            <div class='hero-title'>SIA - Smart Interactive Assistant</div>
            <div class='hero-subtitle'>Organize finanças pessoais, entenda gastos e acompanhe metas com um visual limpo, moderno e pronto para apresentação.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _metric_card(label: str, value: str, note: str, status: str) -> str:
    return (
        f"<div class='metric-card'>"
        f"<div class='metric-label'>{label}</div>"
        f"<div class='metric-value {status}'>{value}</div>"
        f"<div class='metric-note'>{note}</div>"
        f"</div>"
    )


def _summary_card(title: str, description: str, bullets: list[str]) -> str:
    bullet_html = ''.join(f"<li>{item}</li>" for item in bullets)
    return (
        f"<div class='summary-card'>"
        f"<div class='summary-title'>{title}</div>"
        f"<div class='summary-text'>{description}</div>"
        f"<ul class='summary-list'>{bullet_html}</ul>"
        f"</div>"
    )


def _alert_badge(icon: str, text: str, variant: str) -> str:
    return f"<div class='alert-pill {variant}'>{icon}{text}</div>"


def _demo_chart_data() -> pd.DataFrame:
    data = {
        'Categoria': ['Alimentação', 'Transporte', 'Lazer', 'Moradia', 'Educação'],
        'Despesa': [850, 430, 320, 1180, 240],
    }
    return pd.DataFrame(data).set_index('Categoria')


def _render_metrics(modo_demo: bool, receitas_atuais: float, despesas_atuais: float, saldo_atual: float) -> None:
    col1, col2, col3 = st.columns(3, gap='large')
    if modo_demo:
        cards = [
            _metric_card('💵 Receitas', 'Dados protegidos', 'Conteúdo oculto para apresentação.', 'receitas'),
            _metric_card('💸 Despesas', 'Dados protegidos', 'Conteúdo oculto para apresentação.', 'despesas'),
            _metric_card('📊 Saldo', 'Saudável', 'Visão geral positiva de demonstração.', 'saldo'),
        ]
    else:
        cards = [
            _metric_card('💵 Receitas', f'R$ {receitas_atuais:,.2f}', 'Total de receitas registradas.', 'receitas'),
            _metric_card('💸 Despesas', f'R$ {despesas_atuais:,.2f}', 'Total de despesas no período.', 'despesas'),
            _metric_card('📊 Saldo', f'R$ {saldo_atual:,.2f}', 'Saldo líquido disponível.', 'saldo'),
        ]

    for column, card in zip((col1, col2, col3), cards):
        column.markdown(card, unsafe_allow_html=True)


def _render_summary_cards(modo_demo: bool, metas, maiores_categorias: list[tuple[str, float]]) -> None:
    situacao_bullets = [
        'Fluxo de caixa estável',
        'Visão clara da performance financeira',
        'Recomendações de melhoria rápida',
    ]

    metas_bullets = [
        'Metas alinhadas com perfil financeiro',
        'Status atualizado automaticamente',
        'Ajustes sugeridos com base no histórico',
    ]

    categorias_bullets = [
        'Alimentação',
        'Transporte',
        'Lazer',
    ]

    recomendacoes_bullets = [
        'Reveja o orçamento mensal',
        'Mantenha reserva de emergência',
        'Acompanhe metas regularmente',
    ]

    card1 = _summary_card('Situação Financeira', 'Indicadores principais da saúde financeira atual.', situacao_bullets)
    metas_status = len(metas) if not modo_demo else 3
    card2 = _summary_card('Metas Financeiras', f'{metas_status} metas em acompanhamento com recomendações de prioridade.', metas_bullets)
    card3 = _summary_card('Categorias de Gastos', 'As áreas de maior impacto para o seu orçamento.', categorias_bullets)
    card4 = _summary_card('Recomendações', 'Dicas práticas para manter o equilíbrio financeiro.', recomendacoes_bullets)

    col1, col2 = st.columns(2, gap='large')
    col1.markdown(card1, unsafe_allow_html=True)
    col2.markdown(card2, unsafe_allow_html=True)

    col3, col4 = st.columns(2, gap='large')
    col3.markdown(card3, unsafe_allow_html=True)
    col4.markdown(card4, unsafe_allow_html=True)


def _render_alerts(modo_demo: bool, transacoes, metas) -> None:
    st.markdown("<div class='alert-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Alertas</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-description'>Sinais rápidos de saúde financeira para manter o controle sem expor dados sensíveis.</div>", unsafe_allow_html=True)

    if modo_demo:
        st.markdown(_alert_badge('🟡 ', 'Orçamento de alimentação próximo do limite', 'warning'), unsafe_allow_html=True)
        st.markdown(_alert_badge('🟢 ', 'Reserva de emergência em evolução', 'success'), unsafe_allow_html=True)
    else:
        metas_risco = metas_em_risco(transacoes, metas)
        if metas_risco:
            st.markdown(_alert_badge('🟡 ', f'{len(metas_risco)} metas em atenção', 'warning'), unsafe_allow_html=True)
        st.markdown(_alert_badge('🟢 ', 'Reserva de emergência em evolução', 'success'), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _render_demo_chart(modo_demo: bool, transacoes) -> None:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Gráfico de Gastos</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-description'>Distribuição visual de gastos por categoria, em um layout limpo para apresentação.</div>", unsafe_allow_html=True)

    if modo_demo:
        chart_data = _demo_chart_data()
        st.bar_chart(chart_data, use_container_width=True)
        st.markdown("<div class='chart-note'>Dados fictícios exibidos apenas para demonstração visual.</div>", unsafe_allow_html=True)
    else:
        despesas_por_categoria = (
            transacoes[transacoes['tipo'] == 'saida']
            .assign(categoria=lambda df: df['categoria'].fillna('Sem categoria'))
            .groupby('categoria', dropna=False)['valor']
            .sum()
            .sort_values(ascending=False)
        )
        if despesas_por_categoria.empty:
            st.markdown("<div class='summary-text'>Nenhuma despesa registrada para exibir o gráfico.</div>", unsafe_allow_html=True)
        else:
            st.bar_chart(despesas_por_categoria, use_container_width=True)
            st.markdown("<div class='chart-note'>Dados reais agregados por categoria.</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _render_chat_card(transacoes, historico, metas, contexto) -> None:
    if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []

    st.markdown("<div class='chat-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chat-title'>Faça perguntas sobre orçamento, gastos, metas financeiras e educação financeira.</div>", unsafe_allow_html=True)
    st.markdown("<div class='chat-intro'>Converse com a SIA para receber orientações rápidas e contextualizadas de finanças pessoais.</div>", unsafe_allow_html=True)

    if st.session_state.mensagens:
        messages_html = '<div class="chat-messages">'
        for mensagem in st.session_state.mensagens:
            content = html.escape(mensagem['content']).replace('\n', '<br>')
            if mensagem['role'] == 'user':
                messages_html += (
                    '<div class="message-card user">'
                    '<div class="message-role">Você</div>'
                    f'<div class="message-text">{content}</div>'
                    '</div>'
                )
            else:
                messages_html += (
                    '<div class="message-card assistant">'
                    '<div class="message-role">SIA</div>'
                    f'<div class="message-text">{content}</div>'
                    '</div>'
                )
        messages_html += '</div>'
        st.markdown(messages_html, unsafe_allow_html=True)

    with st.form('chat_form'):
        pergunta = st.text_input('Digite sua pergunta:', key='chat_input', placeholder='Escreva sua dúvida financeira aqui', label_visibility='collapsed')
        submit = st.form_submit_button('Enviar')

        if submit and pergunta:
            st.session_state.mensagens.append({'role': 'user', 'content': pergunta})
            with st.spinner('SIA está processando sua pergunta...'):
                resposta = processar_pergunta(pergunta, transacoes, historico, metas, contexto)
            st.session_state.mensagens.append({'role': 'assistant', 'content': resposta})
            st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def renderizar_interface(transacoes, historico, metas, contexto, modo_demo=False) -> None:
    aplicar_estilos()
    _render_hero()

    if modo_demo:
        st.markdown(
            "<div class='demo-banner'><strong>MODO DEMO</strong><span>Valores fictícios exibidos para apresentação. Ideal para screenshots corporativas.</span></div>",
            unsafe_allow_html=True,
        )

    receitas_atuais = calcular_receitas(transacoes)
    despesas_atuais = calcular_despesas(transacoes)
    saldo_atual = calcular_saldo(transacoes)
    maiores_categorias = obter_maiores_categorias(transacoes, 3)

    _render_metrics(modo_demo, receitas_atuais, despesas_atuais, saldo_atual)
    _render_summary_cards(modo_demo, metas, maiores_categorias)
    _render_alerts(modo_demo, transacoes, metas)
    _render_demo_chart(modo_demo, transacoes)
    _render_chat_card(transacoes, historico, metas, contexto)
