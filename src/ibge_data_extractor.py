"""
Módulo para extrair dados econômicos do IBGE de forma paralela.
Extrai informações sobre inflação, desemprego e PIB.

Instalação com UV:
    uv add aiohttp beautifulsoup4

Ou usar o pyproject.toml incluído:
    uv sync
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, Optional, Any
import logging
import sys

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações das URLs e seletores
URLS_CONFIG = {
    'inflacao': {
        'url': 'https://www.ibge.gov.br/explica/inflacao.php',
        'selector': '#dadoBrasil > li:nth-child(2) > p.variavel-dado'
    },
    'desemprego': {
        'url': 'https://www.ibge.gov.br/explica/desemprego.php',
        'selector': '#dadoBrasil > li:nth-child(2) > p.variavel-dado'
    },
    'pib': {
        'url': 'https://www.ibge.gov.br/explica/pib.php',
        'selector': '#dadoBrasil > li.crescimento.variavel > p.variavel-dado'
    }
}

class IBGEDataExtractor:
    """Classe para extrair dados do IBGE de forma assíncrona."""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = None
    
    async def __aenter__(self):
        """Context manager para criar sessão aiohttp."""
        connector = aiohttp.TCPConnector(limit=10)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager para fechar sessão."""
        if self.session:
            await self.session.close()
    
    async def _fetch_and_parse(self, key: str, config: Dict) -> Optional[str]:
        """
        Faz requisição para uma URL e extrai o dado específico.
        
        Args:
            key: Chave do dado (inflacao, desemprego, pib)
            config: Configuração com URL e seletor
            
        Returns:
            Dados extraídos ou None se houve erro
        """
        try:
            async with self.session.get(config['url']) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Encontrar elemento usando seletor CSS
                    element = soup.select_one(config['selector'])
                    if element:
                        data = element.get_text(strip=True)
                        logger.info(f"Dados de {key} extraídos com sucesso: {data}")
                        return data
                    else:
                        logger.warning(f"Elemento não encontrado para {key} com seletor: {config['selector']}")
                        return None
                else:
                    logger.error(f"Erro HTTP {response.status} ao acessar {config['url']}")
                    return None
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout ao acessar {config['url']}")
            return None
        except Exception as e:
            logger.error(f"Erro ao extrair dados de {key}: {str(e)}")
            return None
    
    async def get_all_data(self) -> Dict[str, str]:
        """
        Faz requisições paralelas para todas as URLs e retorna os dados.
        
        Returns:
            Dicionário com os dados extraídos
        """
        tasks = []
        
        # Criar tasks para requisições paralelas
        for key, config in URLS_CONFIG.items():
            task = asyncio.create_task(
                self._fetch_and_parse(key, config),
                name=f"fetch_{key}"
            )
            tasks.append((key, task))
        
        # Aguardar todas as requisições
        results = {}
        for key, task in tasks:
            try:
                result = await task
                results[key] = result or "Dados não disponíveis"
            except Exception as e:
                logger.error(f"Erro na task {key}: {str(e)}")
                results[key] = "Erro na extração"
        
        return results

async def obter_dados_economicos() -> Dict[str, str]:
    """
    Função principal assíncrona para obter dados econômicos do IBGE.
    
    Returns:
        Dicionário com inflação, desemprego e PIB
    """
    async with IBGEDataExtractor() as extractor:
        dados = await extractor.get_all_data()
        
        # Formattar resultado final
        resultado = {
            "inflacao": dados.get("inflacao", "Dados não disponíveis"),
            "desemprego": dados.get("desemprego", "Dados não disponíveis"),
            "pib": dados.get("pib", "Dados não disponíveis")
        }
        
        return resultado

def obter_dados_economicos_sync() -> Dict[str, str]:
    """
    Função síncrona que executa a versão assíncrona.
    Útil para uso em códigos síncronos.
    
    Returns:
        Dicionário com inflação, desemprego e PIB
    """
    try:
        # Verificar se já existe um event loop rodando
        loop = asyncio.get_running_loop()
        # Se existe, usar asyncio.create_task (para usar em contexto assíncrono)
        raise RuntimeError("Use obter_dados_economicos() em contexto assíncrono")
    except RuntimeError:
        # Não há loop rodando, criar um novo
        return asyncio.run(obter_dados_economicos())

# Função de conveniência para importação
def get_economic_data() -> Dict[str, str]:
    """
    Função de conveniência para obter dados econômicos.
    Alias para obter_dados_economicos_sync().
    """
    return obter_dados_economicos_sync()

# Exemplo de uso direto do módulo
if __name__ == "__main__":
    print("🚀 IBGE Data Extractor v1.0.0 (UV)")
    print("=" * 50)
    print("Buscando dados econômicos do IBGE...")
    
    # Verificar se está rodando com UV
    if "uv" in sys.executable or ".venv" in sys.executable:
        print("✅ Rodando com UV")
    else:
        print("⚠️  Recomendado usar UV: uv run python ibge_data_extractor.py")
    
    dados = obter_dados_economicos_sync()
    
    print("\n" + "="*50)
    print("DADOS ECONÔMICOS DO BRASIL")
    print("="*50)
    print(f"💰 Inflação: {dados['inflacao']}")
    print(f"👥 Desemprego: {dados['desemprego']}")
    print(f"📈 PIB: {dados['pib']}")
    print("="*50)
    print("\n💡 Dica: Use 'uv run python exemplo_uso.py' para mais exemplos!")