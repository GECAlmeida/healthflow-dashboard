"""
HealthFlow - Modelo de Machine Learning para Previsão de No-Show
Arquivo: healthflow_model.py
Descrição: Treinamento, validação e predição do modelo Random Forest
Projeto: Mater Dei Challenge 2025 - Sprint 4
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import pickle
import json
from datetime import datetime

class HealthFlowModel:
    """Classe para gerenciar o modelo de previsão de no-show"""
    
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.feature_names = None
        self.metrics = {}
        
    def load_data(self, filepath):
        """Carrega os dados de treinamento"""
        print(f"📂 Carregando dados de {filepath}...")
        df = pd.read_csv(filepath)
        print(f"✅ {len(df)} registros carregados")
        return df
    
    def preprocess_data(self, df):
        """Preprocessa os dados para treinamento"""
        print("\n🔄 Preprocessando dados...")
        
        # Criar cópia para não modificar original
        data = df.copy()
        
        # Converter Data Agendamento para features
        data['Data Agendamento'] = pd.to_datetime(data['Data Agendamento'])
        data['Dia_Semana'] = data['Data Agendamento'].dt.dayofweek
        data['Mes'] = data['Data Agendamento'].dt.month
        
        # Codificar variáveis categóricas
        categorical_cols = ['Especialidade', 'Canal']
        for col in categorical_cols:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            self.encoders[col] = le
        
        # Selecionar features
        self.feature_names = ['Idade', 'Especialidade', 'Canal', 'Dias Antecedência', 'Dia_Semana', 'Mes']
        X = data[self.feature_names]
        
        # Criar variável alvo (inferida do score de risco)
        # Alto risco (score > 66%) = 1 (não comparecerá)
        # Baixo/Moderado risco = 0 (comparecerá)
        y = (data['Score Risco (%)'] > 66).astype(int)
        
        print(f"✅ Features selecionadas: {self.feature_names}")
        print(f"✅ Distribuição da classe: {y.value_counts().to_dict()}")
        
        return X, y
    
    def train_model(self, X, y):
        """Treina o modelo Random Forest"""
        print("\n🤖 Treinando modelo Random Forest...")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Treinar modelo
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        print("✅ Modelo treinado com sucesso")
        
        # Avaliar modelo
        self._evaluate_model(X_train, X_test, y_train, y_test)
        
        return X_test, y_test
    
    def _evaluate_model(self, X_train, X_test, y_train, y_test):
        """Avalia o desempenho do modelo"""
        print("\n📊 Avaliando modelo...")
        
        # Predições
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Métricas de treino
        train_acc = accuracy_score(y_train, y_pred_train)
        print(f"  Acurácia de Treino: {train_acc:.4f}")
        
        # Métricas de teste
        test_acc = accuracy_score(y_test, y_pred_test)
        precision = precision_score(y_test, y_pred_test, zero_division=0)
        recall = recall_score(y_test, y_pred_test, zero_division=0)
        f1 = f1_score(y_test, y_pred_test, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 0
        
        print(f"  Acurácia de Teste: {test_acc:.4f}")
        print(f"  Precisão: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        print(f"  ROC-AUC: {roc_auc:.4f}")
        
        # Armazenar métricas
        self.metrics = {
            'train_accuracy': float(train_acc),
            'test_accuracy': float(test_acc),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'roc_auc': float(roc_auc)
        }
        
        # Matriz de confusão
        cm = confusion_matrix(y_test, y_pred_test)
        print(f"\n  Matriz de Confusão:")
        print(f"    Verdadeiros Negativos: {cm[0, 0]}")
        print(f"    Falsos Positivos: {cm[0, 1]}")
        print(f"    Falsos Negativos: {cm[1, 0]}")
        print(f"    Verdadeiros Positivos: {cm[1, 1]}")
        
        # Importância das features
        print(f"\n  Importância das Features:")
        for feat, importance in zip(self.feature_names, self.model.feature_importances_):
            print(f"    {feat}: {importance:.4f}")
    
    def predict(self, X):
        """Faz predições com o modelo"""
        if self.model is None:
            raise ValueError("Modelo não foi treinado. Execute train_model() primeiro.")
        
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)[:, 1]
        
        return predictions, probabilities
    
    def save_model(self, filepath):
        """Salva o modelo treinado"""
        print(f"\n💾 Salvando modelo em {filepath}...")
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print("✅ Modelo salvo com sucesso")
    
    def load_model(self, filepath):
        """Carrega um modelo treinado"""
        print(f"📂 Carregando modelo de {filepath}...")
        with open(filepath, 'rb') as f:
            loaded_model = pickle.load(f)
        self.model = loaded_model.model
        self.encoders = loaded_model.encoders
        self.feature_names = loaded_model.feature_names
        self.metrics = loaded_model.metrics
        print("✅ Modelo carregado com sucesso")
    
    def save_metrics(self, filepath):
        """Salva as métricas do modelo em JSON"""
        print(f"\n📊 Salvando métricas em {filepath}...")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=False)
        print("✅ Métricas salvas com sucesso")


def main():
    """Função principal para treinar o modelo"""
    
    print("=" * 70)
    print("HealthFlow - Modelo de Previsão de No-Show")
    print("Mater Dei Challenge 2025 - Sprint 4")
    print("=" * 70)
    
    # Criar instância do modelo
    hf_model = HealthFlowModel()
    
    # Carregar dados
    try:
        df = hf_model.load_data('/home/ubuntu/materdei_enriched.csv')
    except FileNotFoundError:
        print("⚠️ Arquivo de dados não encontrado. Usando dados de exemplo...")
        # Gerar dados de exemplo
        df = pd.DataFrame({
            'Idade': np.random.randint(18, 85, 100),
            'Especialidade': np.random.choice(['Cardiologia', 'Pneumologia', 'Oftalmologia'], 100),
            'Canal': np.random.choice(['Online', 'Telefone', 'Presencial'], 100),
            'Dias Antecedência': np.random.randint(1, 30, 100),
            'Data Agendamento': pd.date_range('2026-01-01', periods=100, freq='D'),
            'Score Risco (%)': np.random.uniform(0, 100, 100)
        })
    
    # Preprocessar dados
    X, y = hf_model.preprocess_data(df)
    
    # Treinar modelo
    X_test, y_test = hf_model.train_model(X, y)
    
    # Salvar modelo
    hf_model.save_model('/home/ubuntu/healthflow_model.pkl')
    
    # Salvar métricas
    hf_model.save_metrics('/home/ubuntu/healthflow_metrics.json')
    
    print("\n" + "=" * 70)
    print("✅ Treinamento concluído com sucesso!")
    print("=" * 70)
    
    return hf_model


if __name__ == "__main__":
    model = main()
