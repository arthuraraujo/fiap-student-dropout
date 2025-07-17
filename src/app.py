# src/app.py

import streamlit as st
import pandas as pd
import joblib
import os
from pathlib import Path
from data_fetcher import get_real_time_economic_data # CORRIGIDO

# --- Configuração de Caminhos ---
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
ARTIFACTS_DIR = PROJECT_ROOT / 'artifacts' / 'form_options'
MODEL_PATH = PROJECT_ROOT / 'models' / 'dropout_classifier_v1.pkl'
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed' / 'X_train.csv'

# --- Funções com Cache ---
@st.cache_resource
def load_model(path):
    try:
        return joblib.load(path)
    except FileNotFoundError:
        st.error(f"ERRO: Modelo não encontrado em '{path}'. Certifique-se de que o modelo foi treinado.")
        return None

@st.cache_data
def load_options(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError: return []

@st.cache_data
def get_default_index(options, default_value):
    try: return options.index(default_value)
    except (ValueError, AttributeError): return 0

@st.cache_data
def load_model_columns(path):
    try:
        return pd.read_csv(path).columns.tolist()
    except FileNotFoundError:
        st.error(f"ERRO: Arquivo de colunas do modelo não encontrado em '{path}'. Execute o script de preparação de dados.")
        return []

# --- Interface Principal ---
st.set_page_config(page_title="Previsão de Evasão Estudantil", layout="centered")
st.title("👨‍🎓 Ferramenta de Previsão de Risco de Evasão")
st.write("Preencha os dados do estudante para obter uma análise preditiva. Os dados macroeconômicos podem ser carregados para refletir o contexto atual.")

# --- Lógica de Carregamento Interativo ---
if 'economic_data' not in st.session_state:
    st.session_state.economic_data = {}
if 'loading' not in st.session_state:
    st.session_state.loading = False

st.subheader("Contexto Macroeconômico Atual")

if st.button("Carregar/Atualizar Dados Econômicos em Tempo Real", key="fetch_data"):
    st.session_state.loading = True
    with st.spinner("Buscando dados no Banco Central... Isso pode levar até 20 segundos."):
        st.session_state.economic_data = get_real_time_economic_data()
    st.session_state.loading = False

# --- Exibição dos Dados Macroeconômicos ---
economic_data = st.session_state.economic_data
if economic_data:
    col_inf, col_pib, col_des = st.columns(3)
    def display_metric(column, label, key, unit="%"):
        value = economic_data.get(key)
        if value is not None:
            column.metric(label, f"{value:.2f}{unit}")
        else:
            column.metric(label, "Falhou", delta="API Error", delta_color="off")
            
    display_metric(col_inf, "Inflação (IPCA) Anual", "TaxaInflacao")
    display_metric(col_pib, "PIB (IBC-Br) Anual", "PIB")
    display_metric(col_des, "Taxa de Desemprego", "TaxaDesemprego")
else:
    st.info("Clique no botão acima para carregar os dados macroeconômicos mais recentes.")

# --- Formulário Centralizado ---
with st.form("student_data_form"):
    input_data = {}

    st.subheader("Informações Pessoais e Demográficas")
    col1, col2 = st.columns(2)
    with col1:
        options_ec = load_options(ARTIFACTS_DIR / 'estadocivil_values.txt')
        input_data['EstadoCivil'] = st.selectbox("Estado Civil", options_ec, index=get_default_index(options_ec, "Solteiro"))
        options_nac = load_options(ARTIFACTS_DIR / 'nacionalidade_values.txt')
        input_data['Nacionalidade'] = st.selectbox("Nacionalidade", options=options_nac, index=get_default_index(options_nac, "Português"))
        input_data['Genero'] = st.selectbox("Gênero", options=load_options(ARTIFACTS_DIR / 'genero_values.txt'), index=1)
    with col2:
        input_data['NecessidadesEspeciais'] = 1 if st.radio("Necessidades Especiais?", ('Não', 'Sim'), horizontal=True, index=0) == 'Sim' else 0
        input_data['Bolsista'] = 1 if st.radio("Bolsista?", ('Não', 'Sim'), horizontal=True, index=0) == 'Sim' else 0
        input_data['Devedor'] = 1 if st.radio("Devedor?", ('Não', 'Sim'), horizontal=True, index=0) == 'Sim' else 0
        input_data['MensalidadesEmDia'] = 1 if st.radio("Mensalidades em Dia?", ('Sim', 'Não'), horizontal=True, index=0) == 'Sim' else 0
        input_data['International'] = 1 if st.radio("Internacional?", ('Não', 'Sim'), horizontal=True, index=0) == 'Sim' else 0
    
    st.divider()
    st.subheader("Informações Acadêmicas")
    
    col3, col4 = st.columns(2)
    with col3:
        input_data['Curso'] = st.selectbox("Curso", options=load_options(ARTIFACTS_DIR / 'curso_values.txt'))
        options_qa = ['Ensino Médio', 'Ensino Superior', 'Ensino Superior Incompleto', 'Ensino Técnico/Profissionalizante', 'Ensino Básico', 'Outros']
        input_data['QualificacaoAgrupada'] = st.selectbox("Nível de Qualificação Anterior", options=options_qa, index=get_default_index(options_qa, 'Ensino Médio'))
        input_data['NotaAdmissao'] = st.number_input("Nota de Admissão", value=125.0, step=0.1)
    
    col5, col6 = st.columns(2)
    with col5:
        st.write("**1º Semestre**")
        input_data['UnidadesCurriculares1SemestreCreditado'] = st.number_input("U.C. Creditadas", min_value=0, value=0, key='uc1_cred')
        input_data['UnidadesCurriculares1SemestreInscrito'] = st.number_input("U.C. Inscritas", min_value=0, value=6, key='uc1_insc')
        input_data['UnidadesCurriculares1SemestreAvaliacoes'] = st.number_input("U.C. com Avaliação", min_value=0, value=6, key='uc1_aval')
        input_data['UnidadesCurriculares1SemestreAprovado'] = st.number_input("U.C. Aprovadas", min_value=0, value=5, key='uc1_aprov')
        input_data['UnidadesCurriculares1SemestreGrau'] = st.number_input("Grau Médio", min_value=0.0, value=12.0, step=0.1, key='uc1_grau')
        input_data['UnidadesCurriculares1SemestreSemAvaliacoes'] = st.number_input("U.C. Sem Avaliação", min_value=0, value=0, key='uc1_sem_aval')
    with col6:
        st.write("**2º Semestre**")
        input_data['UnidadesCurriculares2SemestreCreditado'] = st.number_input("U.C. Creditadas", min_value=0, value=0, key='uc2_cred')
        input_data['UnidadesCurriculares2SemestreInscrito'] = st.number_input("U.C. Inscritas", min_value=0, value=6, key='uc2_insc')
        input_data['UnidadesCurriculares2SemestreAvaliacoes'] = st.number_input("U.C. com Avaliação", min_value=0, value=6, key='uc2_aval')
        input_data['UnidadesCurriculares2SemestreAprovado'] = st.number_input("U.C. Aprovadas", min_value=0, value=5, key='uc2_aprov')
        input_data['UnidadesCurriculares2SemestreGrau'] = st.number_input("Grau Médio", min_value=0.0, value=12.0, step=0.1, key='uc2_grau')
        input_data['UnidadesCurriculares2SemestreSemAvaliacoes'] = st.number_input("U.C. Sem Avaliação", min_value=0, value=0, key='uc2_sem_aval')

    st.divider()
    st.subheader("Dados Macroeconômicos para a Previsão")
    col_eco1, col_eco2, col_eco3 = st.columns(3)
    with col_eco1:
        input_data['TaxaInflacao'] = st.number_input("Taxa de Inflação (%)", value=economic_data.get('TaxaInflacao', 1.5))
    with col_eco2:
        input_data['PIB'] = st.number_input("Variação do PIB (%)", value=economic_data.get('PIB', 0.5))
    with col_eco3:
        input_data['TaxaDesemprego'] = st.number_input("Taxa de Desemprego (%)", value=economic_data.get('TaxaDesemprego', 12.0))

    st.divider()
    submitted = st.form_submit_button("Fazer Previsão", type="primary", use_container_width=True)

# --- Lógica de Predição ---
if submitted:
    model = load_model(MODEL_PATH)
    model_columns = load_model_columns(PROCESSED_DATA_PATH)
    
    if model and model_columns:
        input_df = pd.DataFrame([input_data])
        # Converter para one-hot encoding e alinhar colunas com o modelo
        input_df_processed = pd.get_dummies(input_df)
        input_df_reindexed = input_df_processed.reindex(columns=model_columns, fill_value=0)
        
        prediction = model.predict(input_df_reindexed)[0]
        probability = model.predict_proba(input_df_reindexed)[0]
        
        st.subheader("Resultado da Análise")
        prob_desistente = probability[1] # Probabilidade da classe positiva (Evasão)
        
        if prediction == 1:
            st.error(f"ALTO RISCO DE EVASÃO ({prob_desistente:.1%})", icon="🚨")
        else:
            st.success(f"BAIXO RISCO DE EVASÃO ({prob_desistente:.1%})", icon="✅")
            
        st.progress(prob_desistente)
        st.write(f"A probabilidade de o estudante evadir é de **{prob_desistente:.1%}**.")