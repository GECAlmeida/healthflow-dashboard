"""
HealthFlow - Dashboard de Previsão de No-Show
Aplicação Streamlit para visualizar scores de risco de agendamentos
Projeto: Mater Dei Challenge 2025 - Sprint 4
Versão com PDF Export
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from io import BytesIO

# ==================== IMPORTAR REPORTLAB ====================
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

# Configuração da página
st.set_page_config(
    page_title="HealthFlow - Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== FUNÇÕES AUXILIARES ====================

@st.cache_data
def load_data():
    """Carrega os dados dos pacientes"""
    try:
        # Tentar carregar do arquivo JSON (caminho relativo)
        json_path = os.path.join(os.path.dirname(__file__), 'dashboard_data.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            # Garantir que Data Agendamento é datetime
            if 'Data Agendamento' in df.columns:
                df['Data Agendamento'] = pd.to_datetime(df['Data Agendamento'], errors='coerce')
            return df
    except Exception as e:
        pass
    
    # Gerar dados de exemplo se arquivo não existir
    np.random.seed(42)
    df = pd.DataFrame({
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
    return df

def get_risk_color(risk_level):
    """Retorna cor baseada no nível de risco"""
    if risk_level == 'Baixo':
        return '🟢'
    elif risk_level == 'Moderado':
        return '🟡'
    else:
        return '🔴'

def safe_format_date(date_val):
    """Formata data com segurança"""
    try:
        if pd.isna(date_val):
            return 'N/A'
        if isinstance(date_val, str):
            date_val = pd.to_datetime(date_val)
        return date_val.strftime('%d/%m/%Y')
    except:
        return str(date_val)

def generate_pdf_report(filtered_df, df, risk_filter, search_term, sort_by):
    """Gera relatório em PDF"""
    if not HAS_REPORTLAB:
        return None
    
    try:
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
            alignment=1
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#6b7280'),
            spaceAfter=12,
            alignment=1
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
        
        table_data = [['ID', 'Paciente', 'Idade', 'Especialidade', 'Data', 'Score', 'Risco']]
        for _, row in filtered_df.iterrows():
            table_data.append([
                row['ID'],
                row['Nome'][:20],
                str(row['Idade']),
                row['Especialidade'][:15],
                safe_format_date(row['Data Agendamento']),
                f"{row['Score Risco (%)']:.1f}%",
                row['Classificação']
            ])
        
        patients_table = Table(table_data, colWidths=[0.7*inch, 1.3*inch, 0.6*inch, 1.1*inch, 0.8*inch, 0.7*inch, 0.8*inch])
        patients_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(patients_table)
        
        # Rodapé
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("HealthFlow - Sprint 4 | Mater Dei Challenge 2025", styles['Normal']))
        
        # Gerar PDF
        doc.build(elements)
        
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
        return None

# ==================== CARREGAR DADOS ====================
df = load_data()

# Garantir que Data Agendamento é datetime
if 'Data Agendamento' in df.columns and df['Data Agendamento'].dtype != 'datetime64[ns]':
    df['Data Agendamento'] = pd.to_datetime(df['Data Agendamento'], errors='coerce')

# ==================== HEADER ====================
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("# 🏥 HealthFlow")
    st.markdown("### Dashboard de Previsão de No-Show | Mater Dei")

with col2:
    st.markdown("")
    st.markdown("")
    st.info("📊 **Sprint 4 - MVP Final**\n\nDados de Exemplo")

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
    st.metric("🔴 Risco Alto", alto_risco)

with col3:
    moderado_risco = len(df[df['Classificação'] == 'Moderado'])
    st.metric("🟡 Risco Moderado", moderado_risco)

with col4:
    baixo_risco = len(df[df['Classificação'] == 'Baixo'])
    st.metric("🟢 Risco Baixo", baixo_risco)

with col5:
    score_media = df['Score Risco (%)'].mean()
    st.metric("Score Médio", f"{score_media:.1f}%")

st.divider()

# ==================== GRÁFICOS COM STREAMLIT ====================
st.header("📈 Visualizações")

col1, col2 = st.columns(2)

# Gráfico 1: Distribuição de Risco (Bar Chart)
with col1:
    st.subheader("Distribuição de Risco")
    risk_counts = df['Classificação'].value_counts()
    
    # Criar dados para o gráfico
    risk_data = pd.DataFrame({
        'Nível': risk_counts.index,
        'Quantidade': risk_counts.values
    })
    
    st.bar_chart(risk_data.set_index('Nível'))

# Gráfico 2: Score de Risco por Especialidade
with col2:
    st.subheader("Score Médio de Risco por Especialidade")
    specialty_score = df.groupby('Especialidade')['Score Risco (%)'].mean().sort_values(ascending=False)
    
    st.bar_chart(specialty_score)

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

# Converter Data Agendamento com segurança
if len(display_df) > 0:
    display_df['Data Agendamento'] = display_df['Data Agendamento'].apply(safe_format_date)
    display_df['Score Risco (%)'] = display_df['Score Risco (%)'].apply(lambda x: f"{x:.1f}%")
    display_df['Risco'] = display_df['Classificação'].apply(get_risk_color)
    
    # Renomear colunas para exibição
    display_df = display_df[[
        'ID', 'Nome', 'Idade', 'Especialidade', 'Data Agendamento',
        'Score Risco (%)', 'Risco', 'Ação Recomendada'
    ]]
    
    # Exibir tabela
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
            'Risco': st.column_config.TextColumn('Nível', width='small'),
            'Ação Recomendada': st.column_config.TextColumn('Ação Recomendada')
        }
    )
else:
    st.warning("Nenhum agendamento encontrado com os filtros aplicados.")

st.divider()

# ==================== DOWNLOAD ====================
st.header("📄 Exportar Dados")

col1, col2 = st.columns(2)

# Download CSV
with col1:
    export_df = filtered_df.copy()
    
    if len(export_df) > 0:
        export_df['Data Agendamento'] = export_df['Data Agendamento'].apply(safe_format_date)
        export_df['Score Risco (%)'] = export_df['Score Risco (%)'].apply(lambda x: f"{x:.1f}%")
        
        csv = export_df.to_csv(index=False, encoding='utf-8-sig')
        
        st.download_button(
            label="📥 Baixar em CSV",
            data=csv,
            file_name=f"HealthFlow_Dados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("Nenhum dado para exportar com os filtros aplicados.")

# Download PDF
with col2:
    if HAS_REPORTLAB:
        if len(filtered_df) > 0:
            pdf_data = generate_pdf_report(filtered_df, df, risk_filter, search_term, sort_by)
            
            if pdf_data:
                st.download_button(
                    label="📄 Baixar em PDF",
                    data=pdf_data,
                    file_name=f"HealthFlow_Relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.info("Nenhum dado para exportar com os filtros aplicados.")
    else:
        st.warning("⚠️ PDF não disponível nesta versão")

st.divider()

# ==================== ESTATÍSTICAS ADICIONAIS ====================
st.header("📈 Análise Detalhada")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribuição por Especialidade")
    specialty_dist = df['Especialidade'].value_counts()
    st.bar_chart(specialty_dist)

with col2:
    st.subheader("Distribuição por Canal de Agendamento")
    canal_dist = df['Canal'].value_counts()
    st.bar_chart(canal_dist)

st.divider()

# ==================== RODAPÉ ====================
st.markdown("""
---
**HealthFlow** - Solução de Previsão de No-Show para Mater Dei

Sprint 4 - MVP Final | Mater Dei Challenge 2025

Desenvolvido com Python e Streamlit
""")
