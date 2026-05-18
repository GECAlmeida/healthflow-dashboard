"""
HealthFlow - Dashboard de Previsão de No-Show
Aplicação Streamlit para visualizar scores de risco de agendamentos
Projeto: Mater Dei Challenge 2025 - Sprint 4
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os

# Configuração da página
st.set_page_config(
    page_title="HealthFlow - Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS customizado
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .metric-card {
            background-color: #f0f4f8;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #3b82f6;
        }
        .title {
            color: #1f2937;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            color: #6b7280;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def load_data():
    """Carrega os dados dos pacientes"""
    try:
        # Tentar carregar do arquivo JSON (caminho relativo)
        json_path = os.path.join(os.path.dirname(__file__), 'dashboard_data.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return pd.DataFrame(data)
    except Exception as e:
        st.warning(f"Não foi possível carregar arquivo JSON: {e}")
    
    # Gerar dados de exemplo se arquivo não existir
    np.random.seed(42)  # Para reproducibilidade
    return pd.DataFrame({
        'ID': [f'P{i:03d}' for i in range(1, 51)],
        'Nome': [f'Paciente {i}' for i in range(1, 51)],
        'Idade': np.random.randint(18, 85, 50),
        'Especialidade': np.random.choice(['Cardiologia', 'Pneumologia', 'Oftalmologia', 'Gastroenterologia'], 50),
        'Canal': np.random.choice(['Online', 'Telefone', 'Presencial'], 50),
        'Dias Antecedência': np.random.randint(1, 30, 50),
        'Data Agendamento': pd.date_range('2026-05-15', periods=50, freq='D'),
        'Score Risco (%)': np.random.uniform(0, 100, 50),
        'Classificação': np.random.choice(['Baixo', 'Moderado', 'Alto'], 50),
        'Ação Recomendada': np.random.choice(['Fluxo padrão', 'SMS 24h', 'SMS + WhatsApp', 'SMS + WhatsApp + Chamada'], 50)
    })

# Carregar dados
df = load_data()

# Converter Data Agendamento para datetime se necessário
if df['Data Agendamento'].dtype == 'object':
    df['Data Agendamento'] = pd.to_datetime(df['Data Agendamento'])

# ==================== HEADER ====================
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="title">HealthFlow</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Dashboard de Previsão de No-Show | Mater Dei</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="text-align: right; color: #6b7280;">
            <p style="margin: 0;"><strong>Sprint 4 - MVP Final</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">Dados de Exemplo</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ==================== SIDEBAR - FILTROS ====================
st.sidebar.header("🔍 Filtros")

# Filtro de Risco
risk_filter = st.sidebar.selectbox(
    "Filtrar por Nível de Risco",
    ["Todos", "Risco Baixo", "Risco Moderado", "Risco Alto"],
    index=0
)

# Filtro de Busca
search_term = st.sidebar.text_input("Buscar por nome ou ID")

# Filtro de Ordenação
sort_by = st.sidebar.selectbox(
    "Ordenar por",
    ["Score (Maior)", "Idade (Maior)", "Data (Mais Próximo)"],
    index=0
)

# Aplicar filtros
filtered_df = df.copy()

# Filtro de risco
if risk_filter != "Todos":
    risk_map = {
        "Risco Baixo": "Baixo",
        "Risco Moderado": "Moderado",
        "Risco Alto": "Alto"
    }
    filtered_df = filtered_df[filtered_df['Classificação'] == risk_map[risk_filter]]

# Filtro de busca
if search_term:
    filtered_df = filtered_df[
        (filtered_df['Nome'].str.lower().str.contains(search_term.lower())) |
        (filtered_df['ID'].str.lower().str.contains(search_term.lower()))
    ]

# Ordenação
if sort_by == "Score (Maior)":
    filtered_df = filtered_df.sort_values('Score Risco (%)', ascending=False)
elif sort_by == "Idade (Maior)":
    filtered_df = filtered_df.sort_values('Idade', ascending=False)
elif sort_by == "Data (Mais Próximo)":
    filtered_df = filtered_df.sort_values('Data Agendamento', ascending=True)

# ==================== ESTATÍSTICAS ====================
st.header("📊 Resumo de Estatísticas")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total de Agendamentos", len(df))

with col2:
    alto_risco = len(df[df['Classificação'] == 'Alto'])
    st.metric("Risco Alto", alto_risco, delta=None)

with col3:
    moderado_risco = len(df[df['Classificação'] == 'Moderado'])
    st.metric("Risco Moderado", moderado_risco, delta=None)

with col4:
    baixo_risco = len(df[df['Classificação'] == 'Baixo'])
    st.metric("Risco Baixo", baixo_risco, delta=None)

with col5:
    score_media = df['Score Risco (%)'].mean()
    st.metric("Score Médio", f"{score_media:.1f}%", delta=None)

st.divider()

# ==================== GRÁFICOS ====================
st.header("📈 Visualizações")

col1, col2 = st.columns(2)

# Gráfico 1: Distribuição de Risco
with col1:
    risk_counts = df['Classificação'].value_counts()
    fig1 = go.Figure(data=[
        go.Pie(
            labels=risk_counts.index,
            values=risk_counts.values,
            marker=dict(colors=['#10b981', '#f59e0b', '#ef4444']),
            textposition='inside',
            textinfo='label+percent'
        )
    ])
    fig1.update_layout(
        title="Distribuição de Risco",
        height=400,
        showlegend=True
    )
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Score de Risco por Especialidade
with col2:
    specialty_score = df.groupby('Especialidade')['Score Risco (%)'].mean().sort_values(ascending=False)
    fig2 = go.Figure(data=[
        go.Bar(
            x=specialty_score.index,
            y=specialty_score.values,
            marker=dict(color=specialty_score.values, colorscale='RdYlGn_r', showscale=False)
        )
    ])
    fig2.update_layout(
        title="Score Médio de Risco por Especialidade",
        xaxis_title="Especialidade",
        yaxis_title="Score Médio (%)",
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ==================== TABELA DE PACIENTES ====================
st.header("👥 Lista de Agendamentos")

# Informações sobre os filtros aplicados
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"📋 Exibindo {len(filtered_df)} de {len(df)} agendamentos")
with col2:
    if search_term:
        st.info(f"🔍 Busca: '{search_term}'")
with col3:
    if risk_filter != "Todos":
        st.info(f"⚠️ Filtro: {risk_filter}")

# Preparar dados para exibição
display_df = filtered_df.copy()
display_df['Data Agendamento'] = display_df['Data Agendamento'].dt.strftime('%d/%m/%Y')
display_df['Score Risco (%)'] = display_df['Score Risco (%)'].apply(lambda x: f"{x:.1f}%")

# Renomear colunas para exibição
display_df = display_df[[
    'ID', 'Nome', 'Idade', 'Especialidade', 'Data Agendamento',
    'Score Risco (%)', 'Classificação', 'Ação Recomendada'
]]

# Exibir tabela com estilo
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        'ID': st.column_config.TextColumn('ID', width='small'),
        'Nome': st.column_config.TextColumn('Paciente'),
        'Idade': st.column_config.NumberColumn('Idade', width='small'),
        'Especialidade': st.column_config.TextColumn('Especialidade'),
        'Data Agendamento': st.column_config.TextColumn('Data'),
        'Score Risco (%)': st.column_config.TextColumn('Score', width='small'),
        'Classificação': st.column_config.TextColumn('Classificação', width='small'),
        'Ação Recomendada': st.column_config.TextColumn('Ação Recomendada')
    }
)

st.divider()

# ==================== GERAR RELATÓRIO ====================
st.header("📄 Gerar Relatório")

if st.button("📥 Gerar Relatório em PDF", use_container_width=True):
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from io import BytesIO
        
        # Criar PDF em memória
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=6,
            alignment=1  # Centralizado
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#6b7280'),
            spaceAfter=12,
            alignment=1  # Centralizado
        )
        
        # Conteúdo do PDF
        elements = []
        
        # Cabeçalho
        elements.append(Paragraph("HealthFlow - Relatório de Agendamentos", title_style))
        elements.append(Paragraph("Previsão de No-Show | Mater Dei", subtitle_style))
        elements.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", subtitle_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Resumo de Estatísticas
        elements.append(Paragraph("Resumo de Estatísticas", styles['Heading2']))
        summary_data = [
            ['Métrica', 'Valor'],
            ['Total de Agendamentos', str(len(df))],
            ['Risco Alto', str(len(df[df['Classificação'] == 'Alto']))],
            ['Risco Moderado', str(len(df[df['Classificação'] == 'Moderado']))],
            ['Risco Baixo', str(len(df[df['Classificação'] == 'Baixo']))],
            ['Score Médio', f"{df['Score Risco (%)'].mean():.1f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Filtros Aplicados
        elements.append(Paragraph("Filtros Aplicados", styles['Heading2']))
        filters_text = f"""
        <b>Risco:</b> {risk_filter}<br/>
        <b>Busca:</b> {search_term if search_term else 'Nenhuma'}<br/>
        <b>Ordenação:</b> {sort_by}
        """
        elements.append(Paragraph(filters_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Tabela de Pacientes
        elements.append(Paragraph(f"Lista de Pacientes ({len(filtered_df)})", styles['Heading2']))
        
        table_data = [['ID', 'Paciente', 'Idade', 'Especialidade', 'Score', 'Classificação']]
        for _, row in filtered_df.iterrows():
            table_data.append([
                row['ID'],
                row['Nome'][:20],
                str(row['Idade']),
                row['Especialidade'][:15],
                f"{row['Score Risco (%)']:.1f}%",
                row['Classificação']
            ])
        
        patients_table = Table(table_data, colWidths=[0.8*inch, 1.5*inch, 0.7*inch, 1.2*inch, 0.8*inch, 1*inch])
        patients_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(patients_table)
        
        # Rodapé
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("HealthFlow - Sprint 4 | Mater Dei Challenge 2025", styles['Normal']))
        
        # Gerar PDF
        doc.build(elements)
        
        # Baixar PDF
        buffer.seek(0)
        st.download_button(
            label="⬇️ Baixar Relatório PDF",
            data=buffer.getvalue(),
            file_name=f"HealthFlow_Relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
        st.success("✅ Relatório gerado com sucesso!")
        
    except ImportError:
        st.warning("⚠️ Biblioteca reportlab não instalada. Usando alternativa em CSV.")
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Baixar Dados em CSV",
            data=csv,
            file_name=f"HealthFlow_Dados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

st.divider()

# ==================== RODAPÉ ====================
st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.9rem; margin-top: 2rem;">
        <p><strong>HealthFlow</strong> - Solução de Previsão de No-Show para Mater Dei</p>
        <p>Sprint 4 - MVP Final | Mater Dei Challenge 2025</p>
        <p>Desenvolvido com Python, Streamlit e Machine Learning</p>
    </div>
""", unsafe_allow_html=True)
