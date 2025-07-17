# analise_valores.py

import os
import pandas as pd
from pathlib import Path

# --- Configuração de Caminhos (CORRIGIDO) ---
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_CSV_PATH = PROJECT_ROOT / 'data' / 'raw' / 'data.csv'
OUTPUT_DIR = PROJECT_ROOT / 'artifacts' / 'form_options'

def extrair_valores_unicos():
    """
    Carrega um arquivo CSV, identifica colunas categóricas e salva os valores
    únicos de cada uma em arquivos de texto separados.
    """
    print("🔍 Iniciando a análise do CSV para extrair valores únicos...")

    # 1. Verificar se o arquivo de entrada existe
    if not os.path.exists(INPUT_CSV_PATH):
        print(f"❌ ERRO: O arquivo de entrada '{INPUT_CSV_PATH}' não foi encontrado.")
        print("Por favor, verifique o caminho e a estrutura do projeto.")
        return

    # 2. Criar o diretório de saída se ele não existir
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print(f"📂 Diretório de saída '{OUTPUT_DIR}' pronto.")
    except OSError as e:
        print(f"❌ ERRO: Não foi possível criar o diretório de saída: {e}")
        return

    # 3. Carregar o CSV usando pandas
    print(f"📊 Carregando dados de '{INPUT_CSV_PATH}'...")
    try:
        df = pd.read_csv(INPUT_CSV_PATH)
        print("✅ Dados carregados com sucesso!")
    except Exception as e:
        print(f"❌ ERRO: Falha ao carregar o CSV: {e}")
        return

    # 4. Identificar colunas de texto (categóricas)
    colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns
    print(f"\n🎨 Identificadas {len(colunas_categoricas)} colunas de texto para análise: {list(colunas_categoricas)}\n")

    # 5. Iterar e salvar os valores
    for coluna in colunas_categoricas:
        print(f"   - Processando coluna: '{coluna}'...")
        valores_unicos = sorted(df[coluna].dropna().unique().tolist())
        nome_arquivo = f"{coluna.replace(' ', '_').lower()}_values.txt"
        caminho_arquivo_saida = os.path.join(OUTPUT_DIR, nome_arquivo)

        try:
            with open(caminho_arquivo_saida, 'w', encoding='utf-8') as f:
                for valor in valores_unicos:
                    f.write(f"{valor}\n")
            print(f"     ✅ Valores únicos salvos em '{caminho_arquivo_saida}'")
        except IOError as e:
            print(f"     ❌ ERRO: Falha ao salvar o arquivo para a coluna '{coluna}': {e}")
            
    print("\n✅ Processo concluído com sucesso!")

if __name__ == "__main__":
    extrair_valores_unicos()