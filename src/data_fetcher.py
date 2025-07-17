# src/data_fetcher.py (Versão 2 - Timeout Aumentado)

import requests
import pandas as pd
from datetime import datetime

SERIES_CODES = {
    'TaxaInflacao': 13522,
    'TaxaJurosSelic': 432,
    'PIB': 24368,
    'TaxaDesemprego': 24369
}

def fetch_sgs_data(series_code):
    """Busca o último valor de uma série temporal do Banco Central."""
    # Aumentando o timeout para 20 segundos para mais robustez
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_code}/dados/ultimos/1?formato=json"
    try:
        # Timeout aumentado para 20 segundos
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]['valor'])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados para a série {series_code}: {e}")
    except (KeyError, IndexError, ValueError) as e:
        print(f"Erro ao processar os dados da série {series_code}: {e}")
    return None

def get_real_time_economic_data():
    """Busca todos os indicadores macroeconômicos em tempo real."""
    print(f"Buscando dados macroeconômicos do Banco Central... ({datetime.now()})")
    
    economic_data = {key: fetch_sgs_data(code) for key, code in SERIES_CODES.items()}
    
    final_data = {
        'TaxaInflacao': economic_data.get('TaxaInflacao'),
        'TaxaJuros': economic_data.get('TaxaJurosSelic'),
        'PIB': economic_data.get('PIB'),
        'TaxaDesemprego': economic_data.get('TaxaDesemprego')
    }
    
    return final_data