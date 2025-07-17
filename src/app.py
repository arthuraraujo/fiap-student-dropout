# src/app.py (Versão Final - Carregamento Interativo e Resiliente)

import streamlit as st
import pandas as pd
import joblib
import os
from data_fetcher import get_real_time_economic_data

# --- Configuração de Caminhos ---
ARTIFACTS_DIR = '../artifacts/form_options/'
MODEL_PATH = '../models/dropout_classifier_v1.pkl'
PROCESSED_DATA_PATH = '../data/processed/X_train.csv'

# --- Funções com Cache ---
@st.cache_resource
def load_model(path):
    try:
        return joblib.load(path)
    except FileNotFoundError:
        st.error(f"ERRO: Modelo não encontrado em '{path}'.")
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
    except ValueError: return 0

@st.cache_data
def load_model_columns(path):
    try: return pd.read_csv(path).columns.tolist()
    except FileNotFoundError: return []

# --- Interface Principal ---
st.set_page_config(page_title="Previsão de Evasão Estudantil", layout="centered")
st.title("🎓 Ferramenta de Previsão de Risco de Evasão")
st.write("Preencha os dados do estudante para obter uma análise preditiva. Os dados macroeconômicos podem ser carregados para refletir o contexto atual.")

# --- Lógica de Carregamento Interativo ---
# Inicializa o estado da sessão se não existir
if 'economic_data' not in st.session_state:
    st.session_state.economic_data = {}
if 'loading' not in st.session_state:
    st.session_state.loading = False

st.subheader("Contexto Macroeconômico Atual")

# O botão agora controla o início da busca de dados
if st.button("Carregar/Atualizar Dados Econômicos em Tempo Real", key="fetch_data"):
    st.session_state.loading = True
    with st.spinner("Buscando dados no Banco Central... Isso pode levar até 20 segundos."):
        st.session_state.economic_data = get_real_time_economic_data()
    st.session_state.loading = False

# --- Exibição dos Dados Macroeconômicos ---
economic_data = st.session_state.economic_data
if economic_data:
    col_inf, col_jur, col_pib, col_des = st.columns(4)
    # Função auxiliar para mostrar métrica ou erro
    def display_metric(column, label, key, unit="%"):
        value = economic_data.get(key)
        if value is not None:
            column.metric(label, f"{value:.2f}{unit}")
        else:
            column.metric(label, "Falhou", delta="API Timeout", delta_color="off")
            
    display_metric(col_inf, "Inflação (IPCA) Anual", "TaxaInflacao")
    display_metric(col_jur, "Taxa de Juros (Selic)", "TaxaJuros")
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
        options_ec = load_options(os.path.join(ARTIFACTS_DIR, 'estadocivil_values.txt'))
        input_data['EstadoCivil'] = st.selectbox("Estado Civil", options_ec, index=get_default_index(options_ec, "Solteiro"))
        options_nac = load_options(os.path.join(ARTIFACTS_DIR, 'nacionalidade_values.txt'))
        input_data['Nacionalidade'] = st.selectbox("Nacionalidade", options=options_nac, index=get_default_index(options_nac, "Brasileira"))
        input_data['Genero'] = st.selectbox("Gênero", options=load_options(os.path.join(ARTIFACTS_DIR, 'genero_values.txt')))
    with col2:
        input_data['NecessidadesEspeciais'] = 1 if st.radio("Necessidades Especiais?", ('Não', 'Sim'), horizontal=True) == 'Sim' else 0
        input_data['Bolsista'] = 1 if st.radio("Bolsista?", ('Não', 'Sim'), horizontal=True) == 'Sim' else 0
        input_data['Devedor'] = 1 if st.radio("Devedor?", ('Não', 'Sim'), horizontal=True) == 'Sim' else 0
        input_data['MensalidadesEmDia'] = 1 if st.radio("Mensalidades em Dia?", ('Sim', 'Não'), horizontal=True) == 'Sim' else 0
        input_data['International'] = 1 if st.radio("Internacional?", ('Não', 'Sim'), horizontal=True) == 'Sim' else 0
    
    st.divider()
    st.subheader("Informações Acadêmicas")
    # ... (demais campos do formulário)...
    col3, col4 = st.columns(2)
    with col3:
        input_data['Curso'] = st.selectbox("Curso", options=load_options(os.path.join(ARTIFACTS_DIR, 'curso_values.txt')))
        input_data['QualificacaoAgrupada'] = st.selectbox("Nível de Qualificação Anterior", options=['Ensino Médio', 'Ensino Superior', 'Ensino Superior Incompleto', 'Ensino Técnico/Profissionalizante', 'Ensino Básico', 'Outros'])
        input_data['NotaAdmissao'] = st.number_input("Nota de Admissão", value=125.0, step=0.1)
    col5, col6 = st.columns(2)
    with col5:
        st.text("1º Semestre")
        input_data['UnidadesCurriculares1SemestreCreditado'] = st.number_input("U.C. Creditadas", min_value=0, value=0, key='uc1_cred')
        input_data['UnidadesCurriculares1SemestreInscrito'] = st.number_input("U.C. Inscritas", min_value=0, value=6, key='uc1_insc')
        input_data['UnidadesCurriculares1SemestreAvaliacoes'] = st.number_input("U.C. com Avaliação", min_value=0, value=6, key='uc1_aval')
        input_data['UnidadesCurriculares1SemestreAprovado'] = st.number_input("U.C. Aprovadas", min_value=0, value=0, key='uc1_aprov')
        input_data['UnidadesCurriculares1SemestreGrau'] = st.number_input("Grau Médio", min_value=0.0, value=10.0, step=0.1, key='uc1_grau')
        input_data['UnidadesCurriculares1SemestreSemAvaliacoes'] = st.number_input("U.C. Sem Avaliação", min_value=0, value=0, key='uc1_sem_aval')
    with col6:
        st.text("2º Semestre")
        input_data['UnidadesCurriculares2SemestreCreditado'] = st.number_input("U.C. Creditadas", min_value=0, value=0, key='uc2_cred')
        input_data['UnidadesCurriculares2SemestreInscrito'] = st.number_input("U.C. Inscritas", min_value=0, value=6, key='uc2_insc')
        input_data['UnidadesCurriculares2SemestreAvaliacoes'] = st.number_input("U.C. com Avaliação", min_value=0, value=6, key='uc2_aval')
        input_data['UnidadesCurriculares2SemestreAprovado'] = st.number_input("U.C. Aprovadas", min_value=0, value=0, key='uc2_aprov')
        input_data['UnidadesCurriculares2SemestreGrau'] = st.number_input("Grau Médio", min_value=0.0, value=10.0, step=0.1, key='uc2_grau')
        input_data['UnidadesCurriculares2SemestreSemAvaliacoes'] = st.number_input("U.C. Sem Avaliação", min_value=0, value=0, key='uc2_sem_aval')

    st.divider()
    st.subheader("Dados Macroeconômicos para a Previsão")
    # Lógica de Fallback: se o dado não foi carregado, mostra um campo para input manual.
    if economic_data and economic_data.get('TaxaInflacao') is not None:
        input_data['TaxaInflacao'] = economic_data['TaxaInflacao']
    else:
        st.warning("Busca automática de Inflação falhou.", icon="⚠️")
        input_data['TaxaInflacao'] = st.number_input("Insira a Taxa de Inflação (%) Manualmente", value=5.0)

    if economic_data and economic_data.get('PIB') is not None:
        input_data['PIB'] = economic_data['PIB']
    else:
        st.warning("Busca automática de PIB falhou.", icon="⚠️")
        input_data['PIB'] = st.number_input("Insira a Variação do PIB (%) Manualmente", value=1.0)

    if economic_data and economic_data.get('TaxaDesemprego') is not None:
        input_data['TaxaDesemprego'] = economic_data['TaxaDesemprego']
    else:
        st.warning("Busca automática de Desemprego falhou.", icon="⚠️")
        input_data['TaxaDesemprego'] = st.number_input("Insira a Taxa de Desemprego (%) Manualmente", value=9.0)

    st.divider()
    submitted = st.form_submit_button("Fazer Previsão", type="primary", use_container_width=True)

# --- Lógica de Predição ---
if submitted:
    model = load_model(MODEL_PATH)
    model_columns = load_model_columns(PROCESSED_DATA_PATH)
    if model and model_columns:
        input_df = pd.DataFrame([input_data])
        input_df_processed = pd.get_dummies(input_df)
        input_df_reindexed = input_df_processed.reindex(columns=model_columns, fill_value=0)
        
        prediction = model.predict(input_df_reindexed)[0]
        probability = model.predict_proba(input_df_reindexed)[0]
        
        st.subheader("Resultado da Análise")
        prob_desistente = probability[1]
        if prediction == 1:
            st.error(f"ALTO RISCO DE EVASÃO ({prob_desistente:.1%})", icon="🚨")
        else:
            st.success(f"BAIXO RISCO DE EVASÃO ({prob_desistente:.1%})", icon="✅")
        st.progress(prob_desistente)