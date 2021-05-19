import streamlit as st
import pandas as pd
import numpy as np

st.title('Análise de Devedores Qualificados')
st.write("Este aplicativo permite fazer uma avaliação de possíveis candidatos a cobrança qualificada baseada em algoritmos de aprendizagem de máquina semi supervisionado.")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

@st.cache
def get_data():
    return pd.read_csv('dfs/intersection_cluster_NAFE_01_02.csv', usecols=lista_colunas)

st.subheader("Informe o(s) núclo(es) e a comarca da qual faz parte")
opcoes_nucleos = st.multiselect('Informe o(s) núclo(es) do qual faz parte:',
                             ['PROIN - Procuradoria do Interior',
                              'PROFIS-NAFE - Núcleo de Ações Fiscais Estratégicas',
                              'PROFIS-NEF - Núcleo de Execução Fiscal',
                              'PROFIS-NRJ - Núcleo de Representação Judicial'],
                             [])

opcoes_comarca = st.multiselect('Informe sua comarca de atuação:',
                             ['Salvador',
                              'Feira de Santana',
                              'Vitoria da Conquista',
                              'Jequié',
                              ],
                             ["Salvador"])
    #st.write('You selected:', options)

st.subheader("1) Dados Candidatos")
st.write("Sua comarca ainda tem 17 candidatos não avaliados")
lista_colunas = ['CNPJ_base', 'Razão Social']
data2 = pd.read_csv("dfs/cluster_complementar_NAFE_01complementar_01.csv", usecols = lista_colunas)

if st.checkbox("Ver conjunto de dados:"):
    st.write(data2)

if st.checkbox("Ver sumário dos dados"):
    info_dados = data2.describe()
    st.write(info_dados)



st.subheader('2) Selecione quem analisar:')
st.write('Comarca: Salvador')

opcoes = ["Razão Social", "CNPJ"]


select_razao = st.selectbox('Digite a Razão Social ou CNPJ:', data2["Razão Social"])
selected_rows = data2.loc[data2["Razão Social"] == select_razao]

st.write('Razão Social Selecionada:', selected_rows)


with st.sidebar:

    st.info( "🎈 **NOVIDADE:** Você agora deve esolher que quais núcleos você faz parte, antes de realizar sua avaliação..")

    st.header('Passos para sua Avaliação:')



    st.markdown("""
        - Para fazer sua avaliação identifique as informações em documentos, autos do processo, e/ou em sistemas (ex. PGE.NET, Sigat, etc.) 
        - Na coluna principal, marque as respostas e faça observações de sua avaliação (se for o caso)
        - Atribua um score de aderência a uma qualificação do devedor, de 1 a 5, sendo 1 muito baixo e muito alto.
        
        
        [ver minhas avaliações](#)
    """)


# PERGUNTAS


st.write('### 3) Pontue as razões da sua avaliação')
resp_01 = ["Sim", "Não"]
st.radio('Há dificuldade de localização do devedor para citação (de preferência, usar processos mais recentes como referência)?', resp_01)

resp_02 = ["Sim", "Não"]
q01 = st.empty()
q01.radio('No geral, o devedor apresenta garantia nas execuções (independente do tipo)?', resp_02, 0)


resp_03 = ["Sim", "Não"]
st.radio('Caso POSITIVA a resposta anterior, a garantia apresentada nas execuções é boa(dinheiro, fiança ou seguro garantia)?', resp_01)

resp_04 = ["Sim", "Não"]
st.radio('Caso negativa a resposta anterior, a garantia apresentada foi aceita?', resp_02)


resp_05 = ["Sim", "Não"]
st.radio('Já houve tentativa de Bacen-Jud em face do devedor?', resp_01)

resp_06 = ["Sim, totalmente",
           "Sim, parcialmente (acima de 50% do valor do débito)",
           "Sim, parcialmente (abaixo de 50% do valor do débito)",
           "Não"]

st.radio('Caso Positiva a resposta anterior, a ordem foi frutífera?', resp_06)




st.write('### 4) Complemente sua avaliação:')
st.write('Observações sobre sua avaliação que extrapolam as prguntas acima.')
obs = st.text_area("Conclusão da Avaliação:", "Sua observação")



st.write('### 5) Score Final:')
st.write('Atribua um score para sua percepção para a qualificação do devedor, sendo 1 um score muito baixo, e 5 muito alto')
score_aderencia = st.slider(label='Socre Aderência:', min_value=0, max_value=5, value=0, step=1, format='%f')

submeter = st.button("Submeter Avaliação")
st.markdown("""
[ver minhas avaliações](#)
""")