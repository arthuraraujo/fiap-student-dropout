# src/prepare_data.py

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from pathlib import Path # Adicionado

# --- Configuração de Caminhos (CORRIGIDO) ---
# Constrói o caminho absoluto a partir da localização do script
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
RAW_DATA_PATH = PROJECT_ROOT / 'data' / 'raw' / 'data.csv'
PROCESSED_DATA_DIR = PROJECT_ROOT / 'data' / 'processed'

# --- Parâmetros ---
TARGET_COLUMN = 'Target'
POSITIVE_CLASS = 'Desistente'
NEGATIVE_CLASS = 'Graduado'
TEST_SET_SIZE = 0.2
RANDOM_STATE = 42

def mapear_qualificacao(qualificacao):
    """Agrupa as qualificações detalhadas em categorias mais amplas."""
    if 'Ensino superior' in qualificacao or 'bacharelato' in qualificacao or 'licenciatura' in qualificacao or 'mestrado' in qualificacao or 'doutoramento' in qualificacao:
        return 'Ensino Superior'
    if 'Ensino Secundário' in qualificacao or '12º ano' in qualificacao:
        return 'Ensino Médio'
    if 'Tecnológico' in qualificacao or 'tecnológica' in qualificacao:
        return 'Ensino Técnico/Profissionalizante'
    if 'Ensino básico' in qualificacao:
        return 'Ensino Básico'
    if 'Frequência de ensino superior' in qualificacao:
        return 'Ensino Superior Incompleto'
    return 'Outros'

def main():
    """Orquestra o pipeline completo de preparação de dados com engenharia de features."""
    print("🚀 Iniciando o pipeline de preparação de dados (v4)...")
    
    # --- Carregamento dos Dados ---
    try:
        df = pd.read_csv(RAW_DATA_PATH)
        print("✅ Dados brutos carregados.")
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo não encontrado em '{RAW_DATA_PATH}'.")
        return

    # --- Limpeza da Variável Alvo ---
    print("🧹 Limpando a coluna alvo...")
    df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(str).str.strip()
    expected_values = [POSITIVE_CLASS, NEGATIVE_CLASS]
    df = df[df[TARGET_COLUMN].isin(expected_values)].copy()
    df[TARGET_COLUMN] = df[TARGET_COLUMN].map({POSITIVE_CLASS: 1, NEGATIVE_CLASS: 0})
    print("✅ Coluna alvo limpa e mapeada.")

    # --- Engenharia de Features (Nova Etapa) ---
    print("✨ Realizando engenharia de features para 'QualificacaoAnterior'...")
    df['QualificacaoAgrupada'] = df['QualificacaoAnterior'].apply(mapear_qualificacao)
    
    # Remove as colunas originais para evitar redundância e simplificar o modelo
    df.drop(['QualificacaoAnterior', 'QualificacaoAnteriorGrau'], axis=1, inplace=True)
    print("   - Nova feature 'QualificacaoAgrupada' criada.")
    print("   - Colunas originais 'QualificacaoAnterior' e 'QualificacaoAnteriorGrau' removidas.")

    # --- Pré-processamento das Features ---
    print("⚙️ Realizando pré-processamento (imputação e encoding)...")
    X = df.drop(TARGET_COLUMN, axis=1)
    y = df[TARGET_COLUMN]
    
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns
    
    imputer_numerical = SimpleImputer(strategy='median')
    X[numerical_cols] = imputer_numerical.fit_transform(X[numerical_cols])
    
    imputer_categorical = SimpleImputer(strategy='most_frequent')
    X[categorical_cols] = imputer_categorical.fit_transform(X[categorical_cols])
    
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    print("✅ Pré-processamento concluído.")

    # --- Divisão e Salvamento dos Dados ---
    print("🔪 Separando os dados para treino e teste...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SET_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    X_train.to_csv(os.path.join(PROCESSED_DATA_DIR, 'X_train.csv'), index=False)
    X_test.to_csv(os.path.join(PROCESSED_DATA_DIR, 'X_test.csv'), index=False)
    y_train.to_csv(os.path.join(PROCESSED_DATA_DIR, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(PROCESSED_DATA_DIR, 'y_test.csv'), index=False)
    
    print(f"📦 Arquivos processados salvos em '{PROCESSED_DATA_DIR}'")
    print("\n✅ Pipeline de preparação de dados (v4) concluído!")

if __name__ == "__main__":
    main()