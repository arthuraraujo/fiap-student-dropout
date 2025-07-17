# Fase 3 - Arquitetura ML e Aprendizado

Nome: Arthur Francisco Araújo da Silva

Nick(Discord): afaraujo

RM: rm357855

**Vídeo:** https://fiap03.arthuraraujo.com.br

**Live API:** https://fiap-student-dropout.streamlit.app

---

---


# Sistema Preditivo de Evasão Estudantil

[](https://fiap-student-dropout.streamlit.app/)

### Aplicação Online: [https://fiap-student-dropout.streamlit.app/](https://fiap-student-dropout.streamlit.app/)

-----

## 🚀 Visão Geral do Projeto

Este projeto implementa um sistema de Machine Learning para prever a probabilidade de evasão de estudantes em uma instituição de ensino. O objetivo é fornecer uma ferramenta de apoio à decisão para a gestão acadêmica, permitindo a identificação precoce de alunos em risco e a implementação de ações de retenção proativas.

A solução utiliza um pipeline de dados para processamento e limpeza, um modelo de classificação treinado com `scikit-learn` e uma aplicação web interativa construída com `Streamlit` para realizar previsões em tempo real.

## ✨ Principais Funcionalidades

  * **Limpeza e Preparação de Dados:** Um pipeline robusto que carrega os dados brutos, trata valores faltantes e prepara o dataset para o treinamento.
  * **Engenharia de Features:** Criação de variáveis preditivas relevantes a partir dos dados brutos, como o agrupamento de qualificações anteriores (`QualificacaoAgrupada`) para simplificar e potencializar o modelo.
  * **Integração de Dados Macroeconômicos:** A aplicação busca em tempo real (ou permite a inserção manual) de indicadores como Taxa de Inflação, PIB e Taxa de Desemprego para contextualizar a previsão.
  * **Aplicação Web Interativa (Streamlit):** Uma interface amigável onde é possível inserir as informações de um estudante e obter instantaneamente a probabilidade de risco de evasão, juntamente com uma classificação de "Alto" ou "Baixo" risco.

## 🛠️ Tech Stack

  * **Gerenciamento de Pacotes:** uv
  * **Análise e Manipulação de Dados:** Pandas, NumPy
  * **Machine Learning:** Scikit-learn
  * **Aplicação Web:** Streamlit
  * **Visualização de Dados:** Seaborn, Matplotlib

## 📂 Estrutura do Repositório

```
/
|-- 📂 artifacts/        # Arquivos gerados para opções de formulários
|-- 📂 data/
|   |-- 📂 processed/    # Dados processados para treino e teste
|   |-- 📂 raw/          # Dados brutos originais (data.csv)
|
|-- 📂 models/           # Modelo treinado (.pkl) e gráficos
|
|-- 📂 src/              # Código-fonte principal
|   |-- app.py           # Aplicação Streamlit
|   |-- prepare_data.py  # Script para preparar os dados
|   |-- train_model.py   # Script para treinar o modelo
|   |-- ...              # Outros scripts de suporte
|
|-- .gitignore
|-- Dockerfile           # (Opcional, para conteinerização futura)
|-- pyproject.toml       # Definição do projeto e dependências
|-- uv.lock              # Lockfile de dependências
|-- README.md            # Esta documentação
```

## ⚙️ Como Executar Localmente (Para Treinamento e Desenvolvimento)

Siga esta sequência para preparar os dados, treinar um novo modelo e rodar a aplicação na sua própria máquina.

### Pré-requisitos

  * Python 3.12 ou superior
  * Git

### Passo a Passo

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/arthuraraujo/fiap-student-dropout.git
    cd fiap-student-dropout
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Cria o ambiente na pasta .venv
    uv venv

    # Ativa o ambiente (macOS/Linux)
    source .venv/bin/activate

    # Ativa o ambiente (Windows - PowerShell)
    # .\.venv\Scripts\Activate.ps1
    ```

3.  **Instale todas as dependências:**
    O comando `sync` lê o arquivo `uv.lock` e instala as versões exatas de todos os pacotes necessários.

    ```bash
    uv sync
    ```

4.  **Execute o Pipeline de Preparação e Treinamento:**
    Estes comandos devem ser executados na ordem correta.

    ```bash
    # 1. Gera os arquivos de texto para os menus do formulário
    uv run python src/analise_valores.py

    # 2. Limpa os dados e cria os datasets de treino/teste
    uv run python src/prepare_data.py

    # 3. Treina o modelo e o salva na pasta /models
    uv run python src/train_model.py
    ```

5.  **Inicie a Aplicação Streamlit:**
    Após treinar o modelo, você pode iniciar a aplicação web local.

    ```bash
    uv run streamlit run src/app.py
    ```

    Abra seu navegador e acesse **http://localhost:8501**.