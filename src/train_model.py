# train_model.py

import os
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_auc_score
from pathlib import Path # Adicionado

# --- Configuração de Caminhos (CORRIGIDO) ---
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
PROCESSED_DATA_DIR = PROJECT_ROOT / 'data' / 'processed'
MODEL_OUTPUT_DIR = PROJECT_ROOT / 'models'
MODEL_FILENAME = 'dropout_classifier_v1.pkl'
CONFUSION_MATRIX_FILENAME = 'confusion_matrix_v1.png'

# Parâmetros do Modelo
MODEL_PARAMS = {
    'n_estimators': 100,
    'max_depth': 10,
    'random_state': 42,
    'class_weight': 'balanced'
}

def train_model():
    """
    Orquestra o pipeline de treinamento do modelo.
    """
    print("🧠 Iniciando o pipeline de treinamento do modelo...")

    # --- 1. Carregamento dos Dados ---
    try:
        print(f"📥 Carregando dados do diretório '{PROCESSED_DATA_DIR}'...")
        X_train = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'X_train.csv'))
        y_train = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'y_train.csv'))
        X_test = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'X_test.csv'))
        y_test = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'y_test.csv'))
        print("✅ Dados carregados com sucesso.")
    except FileNotFoundError as e:
        print(f"❌ ERRO: Arquivos de dados não encontrados. Você executou o script 'prepare_data.py' primeiro?")
        print(e)
        return

    # --- 2. Treinamento do Modelo ---
    print(f"🏋️ Treinando o modelo RandomForestClassifier...")
    model = RandomForestClassifier(**MODEL_PARAMS)
    model.fit(X_train, y_train.values.ravel())
    print("✅ Modelo treinado com sucesso.")

    # --- 3. Avaliação do Modelo ---
    print("\n📊 Avaliando a performance do modelo no conjunto de teste...")
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    
    print(f"\n  - Acurácia: {accuracy:.4f}")
    print(f"  - ROC AUC Score: {roc_auc:.4f}")
    
    print("\n  - Relatório de Classificação:")
    print(classification_report(y_test, y_pred, target_names=['Graduado', 'Desistente']))

    # --- 4. Salvando os Artefatos (Modelo e Gráfico) ---
    print("💾 Salvando o modelo treinado e a matriz de confusão...")
    os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)
    
    # Salvar o modelo
    model_path = os.path.join(MODEL_OUTPUT_DIR, MODEL_FILENAME)
    joblib.dump(model, model_path)
    print(f"   - Modelo salvo em: '{model_path}'")

    # Gerar e salvar a Matriz de Confusão
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Graduado', 'Desistente'], yticklabels=['Graduado', 'Desistente'])
    plt.xlabel('Previsão do Modelo')
    plt.ylabel('Valor Real')
    plt.title('Matriz de Confusão')
    
    cm_path = os.path.join(MODEL_OUTPUT_DIR, CONFUSION_MATRIX_FILENAME)
    plt.savefig(cm_path)
    print(f"   - Gráfico da Matriz de Confusão salvo em: '{cm_path}'")
    
    print("\n✅ Pipeline de treinamento concluído!")

if __name__ == "__main__":
    train_model()