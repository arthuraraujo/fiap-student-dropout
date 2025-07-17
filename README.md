# Fase 3 - Arquitetura ML e Aprendizado

Nome: Arthur Francisco Araújo da Silva

Nick(Discord): afaraujo

RM: rm357855

**Vídeo:** https://fiap03.arthuraraujo.com.br

**Live API:** https://fiap-03-live.arthuraraujo.com.br

---

---


# Sistema Preditivo de Evasão Estudantil com MLflow e Streamlit

## 📖 Visão Geral do Projeto

Este projeto implementa um sistema de Machine Learning de ponta a ponta para prever a probabilidade de evasão de alunos em uma instituição de ensino superior. O objetivo principal é fornecer uma ferramenta de apoio à decisão para coordenadores e gestores acadêmicos, permitindo a identificação precoce de estudantes em risco e a implementação de ações de retenção proativas.

A solução utiliza um pipeline de dados robusto, rastreamento de experimentos com **MLflow** para garantir reprodutibilidade e uma aplicação web interativa construída com **Streamlit** para visualização de insights e realização de previsões.

## ✨ Principais Funcionalidades

  * **Validação e Limpeza de Dados:** Pipeline automatizado para corrigir inconsistências, tratar valores faltantes e normalizar dados corrompidos de exportações (ex: números astronômicos de planilhas).
  * **Engenharia de Features Avançada:** Criação de variáveis preditivas de alto valor, como a **Taxa de Aprovação** semestral, para capturar o desempenho acadêmico de forma mais eficaz.
  * **Modelagem de Cenários (A/B):** Treinamento e comparação de dois modelos distintos para responder a diferentes perguntas de negócio:
      * **Modelo A (Destino Final):** Prevê o resultado final (Graduado vs. Desistente), ignorando alunos ativos.
      * **Modelo B (Risco Atual):** Prevê o risco de evasão para a população de alunos ativos, ideal para intervenção precoce.
  * **Rastreamento com MLflow:** Todos os treinamentos são registrados, incluindo parâmetros, métricas e artefatos (gráficos, modelos), permitindo total rastreabilidade e comparação entre experimentos.
  * **Aplicação Web Interativa (Streamlit):**
    1.  **Previsão Comparativa:** Análise do risco de um aluno individual sob a ótica dos dois modelos.
    2.  **Dashboard Analítico:** Visualização dos principais fatores de risco e padrões de evasão na instituição.
    3.  **Simulador de Cenários "E Se...?":** Ferramenta para gestores simularem o impacto de intervenções (ex: conceder bolsa) na probabilidade de evasão de um aluno.

## 🏛️ Arquitetura do Projeto

O fluxo de trabalho do projeto segue uma arquitetura modularizada:

1.  **`scripts/prepare_data.py`**: Ingesta os dados brutos, aplica a limpeza, a engenharia de features e o pré-processamento, salvando os datasets limpos (Cenários A e B).
2.  **`scripts/train_model.py`**: Carrega um dos datasets processados, treina o modelo de classificação, realiza a validação e registra todos os resultados e artefatos no servidor do **MLflow**.
3.  **`mlflow ui`**: Inicia a interface de usuário do MLflow, que permite a visualização e comparação detalhada de todos os experimentos de treinamento.
4.  **`app.py`**: Carrega um modelo escolhido (via MLflow) e o objeto de `scaler`, e serve a aplicação web interativa do **Streamlit**.

## 🛠️ Tech Stack

  * **Análise e Manipulação de Dados:** Pandas, NumPy
  * **Machine Learning:** Scikit-learn
  * **Rastreamento de Experimentos:** MLflow
  * **Aplicação Web:** Streamlit
  * **Visualização de Dados:** Plotly, Matplotlib, Seaborn

## 📂 Estrutura do Repositório

```
/projeto-evasao/
|
|-- 📂 data/
|   |-- 📄 raw/         # Local para o arquivo CSV original
|   |-- 📄 processed/   # Onde os dados processados (treino/teste) são salvos
|
|-- 📂 models/          # Para salvar objetos como scalers e imputers
|
|-- 📂 scripts/
|   |-- 📄 prepare_data.py
|   |-- 📄 train_model.py
|
|-- 📄 app.py           # O código da aplicação Streamlit
|
|-- 📂 mlruns/          # Diretório criado e gerenciado pelo MLflow
|
|-- 📄 requirements.txt # Lista de dependências do projeto
|-- 📄 README.md        # Esta documentação
```

## ⚙️ Setup e Instalação

Para executar este projeto localmente, siga os passos abaixo:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/arthuraraujo/fiap-student-dropout.git
    cd projeto-evasao
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Uso e Workflow

Siga esta sequência para executar o pipeline completo:

1.  **Adicione os Dados:** Coloque seu arquivo de dados brutos (ex: `data.csv`) dentro da pasta `/data/raw/`.

2.  **Execute o Pré-processamento:**

    ```bash
    python scripts/prepare_data.py
    ```

    Isso irá gerar os arquivos de treino e teste processados na pasta `/data/processed/`.

3.  **Inicie a Interface do MLflow:**
    Abra um **novo terminal**, navegue até a pasta do projeto e execute:

    ```bash
    mlflow ui
    ```

    Isso iniciará o servidor de rastreamento. Você pode acessá-lo em seu navegador no endereço `http://127.0.0.1:5000`.

4.  **Treine os Modelos:**
    No seu primeiro terminal, execute o script de treinamento. Você pode modificar o script para escolher entre os cenários A ou B.

    ```bash
    python scripts/train_model.py
    ```

    Após a execução, atualize a página do MLflow para ver seu experimento registrado com todas as métricas e artefatos.

5.  **Inicie a Aplicação Web:**
    Finalmente, execute a aplicação Streamlit:

    ```bash
    streamlit run app.py
    ```

    Acesse o endereço fornecido no terminal (geralmente `http://localhost:8501`) para interagir com a aplicação.

## 📊 Conclusões da Análise (Exemplo)

A análise dos modelos revelou insights cruciais sobre os fatores que influenciam a evasão estudantil:

  * **Modelo B (Risco Atual)** demonstrou ser mais útil para a finalidade de intervenção precoce, pois avalia o risco de alunos ainda ativos no sistema.
  * A feature de engenharia **`TaxaDeAprovacao`** consistentemente apareceu como o fator preditivo de maior importância, confirmando que o desempenho acadêmico recente é o indicador mais forte de risco de evasão.
  * Outros fatores relevantes identificados pelo modelo incluíram ser **bolsista** (fator de proteção) e a **nota de admissão**, sugerindo que o perfil de entrada e o suporte financeiro também desempenham um papel significativo.

