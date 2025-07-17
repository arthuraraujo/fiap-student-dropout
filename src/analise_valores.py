# analise_valores.py

import os
import pandas as pd

# --- Configuração ---
# Altere este caminho para o local do seu arquivo CSV completo.
# Usei o caminho do nosso projeto como exemplo.
INPUT_CSV_PATH = '../data/raw/data.csv' 

# O nome da pasta onde os arquivos de texto com os valores serão salvos.
OUTPUT_DIR = '../artifacts/form_options'

def extrair_valores_unicos():
    """
    Carrega um arquivo CSV, identifica colunas categóricas e salva os valores
    únicos de cada uma em arquivos de texto separados.
    """
    print("🚀 Iniciando a análise do CSV para extrair valores únicos...")

    # 1. Verificar se o arquivo de entrada existe
    if not os.path.exists(INPUT_CSV_PATH):
        print(f"❌ ERRO: O arquivo de entrada '{INPUT_CSV_PATH}' não foi encontrado.")
        print("Por favor, verifique o caminho no topo do script.")
        return

    # 2. Criar o diretório de saída se ele não existir
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print(f"📂 Diretório de saída '{OUTPUT_DIR}' pronto.")
    except OSError as e:
        print(f"❌ ERRO: Não foi possível criar o diretório de saída: {e}")
        return

    # 3. Carregar o CSV usando pandas
    print(f"🔄 Carregando dados de '{INPUT_CSV_PATH}'... (Isso pode levar um momento)")
    try:
        df = pd.read_csv(INPUT_CSV_PATH)
        print("✅ Dados carregados com sucesso!")
    except Exception as e:
        print(f"❌ ERRO: Falha ao carregar o CSV: {e}")
        return

    # 4. Identificar apenas as colunas que são de texto (categóricas)
    colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns
    print(f"\n🔍 Identificadas {len(colunas_categoricas)} colunas de texto para análise: {list(colunas_categoricas)}\n")

    # 5. Iterar sobre cada coluna categórica para extrair e salvar os valores
    for coluna in colunas_categoricas:
        print(f"   - Processando coluna: '{coluna}'...")

        # Pega os valores únicos, remove valores nulos (NaN) e converte para uma lista
        valores_unicos = df[coluna].dropna().unique().tolist()
        
        # Ordena a lista em ordem alfabética para uma melhor experiência no formulário
        valores_ordenados = sorted(valores_unicos)

        # Define um nome de arquivo seguro (minúsculas, sem espaços)
        nome_arquivo = f"{coluna.replace(' ', '_').lower()}_values.txt"
        caminho_arquivo_saida = os.path.join(OUTPUT_DIR, nome_arquivo)

        # Salva a lista em um arquivo de texto, um valor por linha
        try:
            with open(caminho_arquivo_saida, 'w', encoding='utf-8') as f:
                for valor in valores_ordenados:
                    f.write(f"{valor}\n")
            print(f"     ✅ Valores únicos salvos em '{caminho_arquivo_saida}'")
        except IOError as e:
            print(f"     ❌ ERRO: Falha ao salvar o arquivo para a coluna '{coluna}': {e}")
            
    print("\n🎉 Processo concluído com sucesso!")


if __name__ == "__main__":
    extrair_valores_unicos()