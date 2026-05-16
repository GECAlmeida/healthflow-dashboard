"""
HealthFlow - Análise Exploratória de Dados (EDA)
Arquivo: healthflow_eda.py
Descrição: Análise completa dos dados de agendamentos da Mater Dei
Projeto: Mater Dei Challenge 2025 - Sprint 4
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class HealthFlowEDA:
    """Classe para análise exploratória de dados"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.summary = {}
        
    def load_data(self):
        """Carrega os dados"""
        print(f"📂 Carregando dados de {self.filepath}...")
        try:
            self.df = pd.read_csv(self.filepath)
            print(f"✅ {len(self.df)} registros carregados")
            print(f"✅ {len(self.df.columns)} colunas")
            return self.df
        except FileNotFoundError:
            print(f"⚠️ Arquivo não encontrado: {self.filepath}")
            return None
    
    def basic_info(self):
        """Informações básicas dos dados"""
        print("\n" + "=" * 70)
        print("INFORMAÇÕES BÁSICAS")
        print("=" * 70)
        
        print(f"\n📊 Dimensões: {self.df.shape}")
        print(f"📋 Colunas: {list(self.df.columns)}")
        print(f"📅 Período: {self.df['Data Agendamento'].min()} a {self.df['Data Agendamento'].max()}")
        
        print("\n🔍 Tipos de Dados:")
        print(self.df.dtypes)
        
        print("\n📈 Valores Faltantes:")
        missing = self.df.isnull().sum()
        if missing.sum() == 0:
            print("  ✅ Nenhum valor faltante")
        else:
            print(missing[missing > 0])
    
    def statistical_summary(self):
        """Resumo estatístico"""
        print("\n" + "=" * 70)
        print("RESUMO ESTATÍSTICO")
        print("=" * 70)
        
        print("\n📊 Idade:")
        print(f"  Média: {self.df['Idade'].mean():.1f} anos")
        print(f"  Mediana: {self.df['Idade'].median():.1f} anos")
        print(f"  Desvio Padrão: {self.df['Idade'].std():.1f}")
        print(f"  Mínimo: {self.df['Idade'].min()} anos")
        print(f"  Máximo: {self.df['Idade'].max()} anos")
        
        print("\n⚠️ Score de Risco (%):")
        print(f"  Média: {self.df['Score Risco (%)'].mean():.1f}%")
        print(f"  Mediana: {self.df['Score Risco (%)'].median():.1f}%")
        print(f"  Desvio Padrão: {self.df['Score Risco (%)'].std():.1f}")
        print(f"  Mínimo: {self.df['Score Risco (%)'].min():.1f}%")
        print(f"  Máximo: {self.df['Score Risco (%)'].max():.1f}%")
        
        print("\n📅 Dias de Antecedência:")
        print(f"  Média: {self.df['Dias Antecedência'].mean():.1f} dias")
        print(f"  Mediana: {self.df['Dias Antecedência'].median():.1f} dias")
        print(f"  Mínimo: {self.df['Dias Antecedência'].min()} dias")
        print(f"  Máximo: {self.df['Dias Antecedência'].max()} dias")
    
    def categorical_analysis(self):
        """Análise de variáveis categóricas"""
        print("\n" + "=" * 70)
        print("ANÁLISE DE VARIÁVEIS CATEGÓRICAS")
        print("=" * 70)
        
        print("\n🏥 Especialidades:")
        spec_counts = self.df['Especialidade'].value_counts()
        for spec, count in spec_counts.items():
            pct = (count / len(self.df)) * 100
            print(f"  {spec}: {count} ({pct:.1f}%)")
        
        print("\n📱 Canais de Agendamento:")
        canal_counts = self.df['Canal'].value_counts()
        for canal, count in canal_counts.items():
            pct = (count / len(self.df)) * 100
            print(f"  {canal}: {count} ({pct:.1f}%)")
        
        print("\n⚠️ Classificação de Risco:")
        risk_counts = self.df['Classificação'].value_counts()
        for risk, count in risk_counts.items():
            pct = (count / len(self.df)) * 100
            print(f"  {risk}: {count} ({pct:.1f}%)")
    
    def correlation_analysis(self):
        """Análise de correlação"""
        print("\n" + "=" * 70)
        print("ANÁLISE DE CORRELAÇÃO")
        print("=" * 70)
        
        # Selecionar colunas numéricas
        numeric_cols = ['Idade', 'Dias Antecedência', 'Score Risco (%)']
        corr_matrix = self.df[numeric_cols].corr()
        
        print("\n📊 Matriz de Correlação:")
        print(corr_matrix.to_string())
        
        # Correlações com Score de Risco
        print("\n🔗 Correlações com Score de Risco:")
        score_corr = corr_matrix['Score Risco (%)'].sort_values(ascending=False)
        for var, corr in score_corr.items():
            if var != 'Score Risco (%)':
                print(f"  {var}: {corr:.4f}")
    
    def risk_distribution(self):
        """Análise da distribuição de risco"""
        print("\n" + "=" * 70)
        print("ANÁLISE DE DISTRIBUIÇÃO DE RISCO")
        print("=" * 70)
        
        # Score médio por especialidade
        print("\n🏥 Score Médio de Risco por Especialidade:")
        spec_risk = self.df.groupby('Especialidade')['Score Risco (%)'].agg(['mean', 'count']).sort_values('mean', ascending=False)
        for spec, row in spec_risk.iterrows():
            print(f"  {spec}: {row['mean']:.1f}% (n={int(row['count'])})")
        
        # Score médio por canal
        print("\n📱 Score Médio de Risco por Canal:")
        canal_risk = self.df.groupby('Canal')['Score Risco (%)'].agg(['mean', 'count']).sort_values('mean', ascending=False)
        for canal, row in canal_risk.iterrows():
            print(f"  {canal}: {row['mean']:.1f}% (n={int(row['count'])})")
        
        # Score médio por faixa etária
        print("\n👥 Score Médio de Risco por Faixa Etária:")
        self.df['Faixa Etária'] = pd.cut(self.df['Idade'], bins=[0, 30, 40, 50, 60, 100], 
                                          labels=['18-30', '31-40', '41-50', '51-60', '60+'])
        age_risk = self.df.groupby('Faixa Etária')['Score Risco (%)'].agg(['mean', 'count']).sort_values('mean', ascending=False)
        for faixa, row in age_risk.iterrows():
            print(f"  {faixa}: {row['mean']:.1f}% (n={int(row['count'])})")
    
    def generate_visualizations(self, output_dir='/home/ubuntu'):
        """Gera visualizações dos dados"""
        print("\n" + "=" * 70)
        print("GERANDO VISUALIZAÇÕES")
        print("=" * 70)
        
        # 1. Distribuição de Risco
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        risk_counts = self.df['Classificação'].value_counts()
        colors = ['#10b981', '#f59e0b', '#ef4444']
        axes[0].pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%', colors=colors)
        axes[0].set_title('Distribuição de Risco', fontsize=14, fontweight='bold')
        
        # 2. Score de Risco por Especialidade
        spec_risk = self.df.groupby('Especialidade')['Score Risco (%)'].mean().sort_values(ascending=False)
        axes[1].barh(spec_risk.index, spec_risk.values, color='#3b82f6')
        axes[1].set_xlabel('Score Médio de Risco (%)')
        axes[1].set_title('Score de Risco por Especialidade', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/healthflow_eda_1.png', dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico 1 salvo: healthflow_eda_1.png")
        plt.close()
        
        # 3. Distribuição de Idade e Score de Risco
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        axes[0].hist(self.df['Idade'], bins=20, color='#3b82f6', edgecolor='black')
        axes[0].set_xlabel('Idade (anos)')
        axes[0].set_ylabel('Frequência')
        axes[0].set_title('Distribuição de Idade', fontsize=14, fontweight='bold')
        
        axes[1].hist(self.df['Score Risco (%)'], bins=20, color='#ef4444', edgecolor='black')
        axes[1].set_xlabel('Score de Risco (%)')
        axes[1].set_ylabel('Frequência')
        axes[1].set_title('Distribuição de Score de Risco', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/healthflow_eda_2.png', dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico 2 salvo: healthflow_eda_2.png")
        plt.close()
        
        # 4. Scatter plot: Idade vs Score de Risco
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors_map = {'Baixo': '#10b981', 'Moderado': '#f59e0b', 'Alto': '#ef4444'}
        for risk in self.df['Classificação'].unique():
            mask = self.df['Classificação'] == risk
            ax.scatter(self.df[mask]['Idade'], self.df[mask]['Score Risco (%)'], 
                      label=risk, alpha=0.6, s=100, color=colors_map.get(risk, '#999'))
        
        ax.set_xlabel('Idade (anos)', fontsize=12)
        ax.set_ylabel('Score de Risco (%)', fontsize=12)
        ax.set_title('Relação entre Idade e Score de Risco', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/healthflow_eda_3.png', dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico 3 salvo: healthflow_eda_3.png")
        plt.close()
    
    def generate_report(self, output_file='/home/ubuntu/healthflow_eda_report.txt'):
        """Gera um relatório completo da EDA"""
        print(f"\n💾 Salvando relatório em {output_file}...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("HealthFlow - Relatório de Análise Exploratória de Dados (EDA)\n")
            f.write("Mater Dei Challenge 2025 - Sprint 4\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Data do Relatório: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n\n")
            
            # Informações básicas
            f.write("INFORMAÇÕES BÁSICAS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total de Registros: {len(self.df)}\n")
            f.write(f"Total de Colunas: {len(self.df.columns)}\n")
            f.write(f"Período: {self.df['Data Agendamento'].min()} a {self.df['Data Agendamento'].max()}\n\n")
            
            # Resumo estatístico
            f.write("RESUMO ESTATÍSTICO\n")
            f.write("-" * 70 + "\n")
            f.write(f"Idade Média: {self.df['Idade'].mean():.1f} anos\n")
            f.write(f"Score de Risco Médio: {self.df['Score Risco (%)'].mean():.1f}%\n")
            f.write(f"Dias de Antecedência Médio: {self.df['Dias Antecedência'].mean():.1f} dias\n\n")
            
            # Distribuição de risco
            f.write("DISTRIBUIÇÃO DE RISCO\n")
            f.write("-" * 70 + "\n")
            for risk, count in self.df['Classificação'].value_counts().items():
                pct = (count / len(self.df)) * 100
                f.write(f"{risk}: {count} ({pct:.1f}%)\n")
            f.write("\n")
            
            # Especialidades
            f.write("ESPECIALIDADES\n")
            f.write("-" * 70 + "\n")
            for spec, count in self.df['Especialidade'].value_counts().items():
                pct = (count / len(self.df)) * 100
                f.write(f"{spec}: {count} ({pct:.1f}%)\n")
        
        print(f"✅ Relatório salvo: {output_file}")


def main():
    """Função principal"""
    
    print("=" * 70)
    print("HealthFlow - Análise Exploratória de Dados")
    print("Mater Dei Challenge 2025 - Sprint 4")
    print("=" * 70)
    
    # Criar instância da EDA
    eda = HealthFlowEDA('/home/ubuntu/materdei_enriched.csv')
    
    # Carregar dados
    if eda.load_data() is None:
        print("❌ Não foi possível carregar os dados")
        return
    
    # Executar análises
    eda.basic_info()
    eda.statistical_summary()
    eda.categorical_analysis()
    eda.correlation_analysis()
    eda.risk_distribution()
    eda.generate_visualizations()
    eda.generate_report()
    
    print("\n" + "=" * 70)
    print("✅ Análise Exploratória Concluída!")
    print("=" * 70)


if __name__ == "__main__":
    main()
