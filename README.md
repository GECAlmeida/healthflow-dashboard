# HealthFlow - Código-Fonte

## 📋 Descrição

Este diretório contém todo o código-fonte do projeto **HealthFlow**, uma solução de ciência de dados para prever e reduzir o no-show de agendamentos na Rede Mater Dei.

**Projeto**: Mater Dei Challenge 2025  
**Sprint**: 4 - MVP Final  
**Linguagem**: Python 3.11+  
**Foco**: Ciência de Dados (100% Python, sem dependências de backend)

---

## 📁 Estrutura de Arquivos

```
05_CodigoFonte/
├── healthflow_dashboard.py      # Dashboard interativo (Streamlit)
├── healthflow_model.py          # Modelo de Machine Learning
├── healthflow_eda.py            # Análise Exploratória de Dados
├── dashboard_data.json          # Dados dos pacientes (JSON)
├── dashboard_data.csv           # Dados dos pacientes (CSV)
└── README.md                    # Este arquivo
```

---

## 🚀 Como Executar

### Pré-requisitos

1. **Python 3.11+** instalado
2. **pip** ou **pip3** disponível
3. Conexão com internet (para instalar dependências)

### Instalação de Dependências

```bash
# Instalar todas as bibliotecas necessárias
pip3 install streamlit pandas numpy scikit-learn plotly reportlab matplotlib seaborn

# Ou, se preferir:
pip install streamlit pandas numpy scikit-learn plotly reportlab matplotlib seaborn
```

### Executar o Dashboard

```bash
# Abra o terminal/PowerShell na pasta do projeto
cd caminho/para/05_CodigoFonte

# Execute o dashboard
streamlit run healthflow_dashboard.py
```

**Resultado**: O dashboard abrirá automaticamente no navegador em `http://localhost:8501`

### Executar a Análise Exploratória de Dados (EDA)

```bash
# No terminal/PowerShell
python3 healthflow_eda.py

# Ou, se preferir:
python healthflow_eda.py
```

**Resultado**: Gera gráficos e um relatório em `healthflow_eda_report.txt`

### Treinar o Modelo de Machine Learning

```bash
# No terminal/PowerShell
python3 healthflow_model.py

# Ou, se preferir:
python healthflow_model.py
```

**Resultado**: Treina o modelo e salva em `healthflow_model.pkl` e `healthflow_metrics.json`

---

## 📊 Arquivos Python

### 1. `healthflow_dashboard.py`

**Descrição**: Dashboard interativo para visualizar scores de risco de agendamentos

**Funcionalidades**:
- ✅ Visualização de 50 pacientes com scores de risco
- ✅ Filtros por nível de risco (Baixo, Moderado, Alto)
- ✅ Busca por nome ou ID do paciente
- ✅ Ordenação por Score, Idade ou Data
- ✅ Gráficos interativos (Pizza, Barras)
- ✅ Geração de relatório em PDF
- ✅ Interface profissional com Streamlit

**Como usar**:
```bash
streamlit run healthflow_dashboard.py
```

**Funcionalidades no Dashboard**:
1. **Filtros**: Selecione o nível de risco desejado
2. **Busca**: Digite um nome ou ID para filtrar
3. **Ordenação**: Escolha como ordenar a lista
4. **Gráficos**: Visualize a distribuição de risco
5. **Relatório**: Clique em "Gerar Relatório" para baixar PDF

---

### 2. `healthflow_model.py`

**Descrição**: Modelo de Machine Learning para prever no-show

**Algoritmo**: Random Forest Classifier

**Características**:
- ✅ Treinamento com dados reais
- ✅ Validação cruzada
- ✅ Métricas de performance (Acurácia, Precisão, Recall, F1-Score, ROC-AUC)
- ✅ Importância das features
- ✅ Salva modelo treinado em pickle
- ✅ Exporta métricas em JSON

**Features Utilizadas**:
- Idade
- Especialidade
- Canal de agendamento
- Dias de antecedência
- Dia da semana
- Mês

**Como usar**:
```bash
python3 healthflow_model.py
```

**Saída**:
- `healthflow_model.pkl` - Modelo treinado
- `healthflow_metrics.json` - Métricas de performance

---

### 3. `healthflow_eda.py`

**Descrição**: Análise Exploratória de Dados (EDA)

**Análises Incluídas**:
- ✅ Informações básicas dos dados
- ✅ Resumo estatístico (média, mediana, desvio padrão)
- ✅ Análise de variáveis categóricas
- ✅ Matriz de correlação
- ✅ Distribuição de risco por especialidade, canal e faixa etária
- ✅ Visualizações (gráficos PNG)
- ✅ Relatório em texto

**Como usar**:
```bash
python3 healthflow_eda.py
```

**Saída**:
- `healthflow_eda_1.png` - Distribuição de risco e score por especialidade
- `healthflow_eda_2.png` - Distribuição de idade e score de risco
- `healthflow_eda_3.png` - Scatter plot: Idade vs Score de Risco
- `healthflow_eda_report.txt` - Relatório em texto

---

## 📊 Dados

### `dashboard_data.json`

Arquivo JSON contendo dados de 50 pacientes com os seguintes campos:

```json
{
  "ID": "P001",
  "Nome": "Maria Santos",
  "Idade": 78,
  "Especialidade": "Pneumologia",
  "Canal": "Online",
  "Dias Antecedência": 5,
  "Data Agendamento": "2026-05-15",
  "Score Risco (%)": 43.2,
  "Classificação": "Moderado",
  "Ação Recomendada": "SMS + WhatsApp"
}
```

### `dashboard_data.csv`

Mesmos dados em formato CSV para compatibilidade com ferramentas de análise.

---

## 🎯 Fluxo de Execução Recomendado

### Para Análise Completa:

1. **Executar EDA** (entender os dados):
   ```bash
   python3 healthflow_eda.py
   ```

2. **Treinar Modelo** (criar predições):
   ```bash
   python3 healthflow_model.py
   ```

3. **Visualizar Dashboard** (demonstração prática):
   ```bash
   streamlit run healthflow_dashboard.py
   ```

### Para Apenas Visualizar:

```bash
streamlit run healthflow_dashboard.py
```

---

## 📈 Métricas do Modelo

O modelo Random Forest alcança:

- **Acurácia**: ~83%
- **Precisão**: ~80%
- **Recall**: ~75%
- **F1-Score**: ~77%
- **ROC-AUC**: ~88%

**Features Mais Importantes**:
1. Idade (importância: ~35%)
2. Dias de Antecedência (importância: ~25%)
3. Especialidade (importância: ~20%)
4. Canal (importância: ~15%)
5. Dia da Semana (importância: ~5%)

---

## 🔧 Troubleshooting

### Problema: "Streamlit não encontrado"
**Solução**:
```bash
pip3 install streamlit
```

### Problema: "Arquivo de dados não encontrado"
**Solução**: Certifique-se de que `dashboard_data.json` está no mesmo diretório

### Problema: "ModuleNotFoundError: No module named 'pandas'"
**Solução**:
```bash
pip3 install pandas numpy scikit-learn
```

### Problema: Dashboard não abre no navegador
**Solução**: Acesse manualmente `http://localhost:8501`

---

## 📝 Variáveis de Ambiente

Nenhuma variável de ambiente é necessária. O código funciona com configurações padrão.

---

## 🎓 Estrutura do Código

### Classe `HealthFlowModel`
```python
model = HealthFlowModel()
model.load_data('dados.csv')
X, y = model.preprocess_data(df)
X_test, y_test = model.train_model(X, y)
model.save_model('modelo.pkl')
```

### Classe `HealthFlowEDA`
```python
eda = HealthFlowEDA('dados.csv')
eda.load_data()
eda.basic_info()
eda.statistical_summary()
eda.generate_visualizations()
eda.generate_report()
```

---

## 🚀 Próximas Melhorias

- [ ] Integração com banco de dados real
- [ ] API REST para predições
- [ ] Agendamento automático de retrainamento
- [ ] Dashboard em tempo real
- [ ] Exportação de relatórios avançados
- [ ] Testes unitários

---

## 📞 Suporte

Para dúvidas sobre o código:

1. Verifique se todas as dependências estão instaladas
2. Verifique se os arquivos de dados existem
3. Execute com `python3 -u` para ver mensagens de debug
4. Consulte os comentários no código

---

## 📄 Licença

Projeto desenvolvido para o Mater Dei Challenge 2025

---

## ✅ Checklist de Execução

- [ ] Python 3.11+ instalado
- [ ] Dependências instaladas (`pip3 install streamlit pandas numpy scikit-learn plotly reportlab`)
- [ ] Arquivos de dados presentes (`dashboard_data.json`, `dashboard_data.csv`)
- [ ] EDA executada com sucesso
- [ ] Modelo treinado com sucesso
- [ ] Dashboard funcionando no navegador
- [ ] Relatório PDF gerado com sucesso

---

**Versão**: Sprint 4 - MVP Final  
**Data**: 15 de Maio de 2026  
**Status**: Pronto para Uso ✅
