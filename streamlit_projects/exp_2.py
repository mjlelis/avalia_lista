import pandas as pd
import streamlit as st
import unicodecsv as csv
import sqlite3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, insert, select, and_
from login_orm import User, UserInput

# Criando DB


engine = create_engine('sqlite:///reg_db.sqlite3')
Session = sessionmaker(bind=engine)
session = Session()

c = engine.connect()


def add_userdata(username, password, email, setor):
    data_to_add = insert(User).values(user_name=username,
                                      user_pass=password,
                                      user_email=email,
                                      user_sector=setor)
    c.execute(data_to_add)


def login_user(username, password):
    stmt = select([User])
    stmt = stmt.where(
        and_(User.user_name == username,
             User.user_pass == password))
    data = c.execute(stmt).fetchall()

    # return {"tudo":data, "u":username
    return data


def user_sector():
    stmt = select([User])
    stmt = stmt.where(User.user_sector == "proin")
    setor = c.execute(stmt).fetchall()
    for resultado in setor:
        return resultado.user_sector


def active_user():
    stmt = select([User.id])
    id_user = c.execute(stmt).fetchall()
    for ids in id_user:
        return ids.id


def ver_usuarios():
    usuarios = select([User])
    data = c.execute(usuarios).fetchall()
    return data


st.title('Análise de Devedores Qualificados')
st.write(
    "Este aplicativo permite fazer uma avaliação de possíveis candidatos a cobrança qualificada baseada em algoritmos de aprendizagem de máquina semi supervisionado.")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


def exposicao_nucelos():
    def get_data():
        return pd.read_csv('dfs/complementar_para_streamlit_01.csv',
                           usecols=colunas_01,
                           index_col=False
                           )

    lista_colunas = ['CNPJ/CPF Base', 'Razão Social', 'Comarca']

    data0 = pd.read_csv("dfs/complementar_para_streamlit_01.csv", usecols=lista_colunas)
    data2 = pd.read_csv("dfs/complementar_para_streamlit_01.csv", usecols=lista_colunas)
    data3 = pd.read_csv("dfs/complementar_para_streamlit_01.csv", usecols=lista_colunas)

    dados = [data2, data3]

    colunas_01 = ['CNPJ/CPF Base', 'Razão Social', 'Comarca']

    df = get_data()

    st.subheader("Informe o(s) núclo(es) e a comarca da qual faz parte")
    nucleos = ['PROIN - Procuradoria do Interior',
               'PROFIS-NAFE - Núcleo de Ações Fiscais Estratégicas',
               'PROFIS-NEF - Núcleo de Execução Fiscal',
               'PROFIS-NRJ - Núcleo de Representação Judicial']
    opcoes_nucleos = st.selectbox('Informe o(s) núclo(es) do qual faz parte:',
                                  options=nucleos)



    comarcas = df["Comarca"].unique()
    comarcas_proin = df["Comarca"].loc[(df["Comarca"] != "SALVADOR") & \
                                       (df["Comarca"] != "LAURO DE FREITAS") & \
                                       (df["Comarca"] != "Comarca de Simões Filho") & \
                                       (df["Comarca"] != 'CAMAÇARI') & \
                                       (df["Comarca"] != 'CANDEIAS') & \
                                       (df["Comarca"] != 'DIAS D AVILA') & \
                                       (df["Comarca"] != 'SIMOES FILHO') & \
                                       (df["Comarca"] != 'Comarca de Salvador') & \
                                       (df["Comarca"] != 'Comarca de Lauro De Freitas') & \
                                       (df["Comarca"] != 'Comarca de Dias D ?vila') & \
                                       (df["Comarca"] != 'Comarca de Cama?ari') & \
                                       (df["Comarca"] != 'Comarca de Camaçari') & \
                                       (df["Comarca"] != 'Lauro De Freitas')

                                       ].unique()

    if opcoes_nucleos == 'PROIN - Procuradoria do Interior':

        opcoes_comarca = st.selectbox("Selecione sua comarca de atuação",
                                      options=comarcas_proin)

        st.subheader("1) Dados Candidatos")
        if st.checkbox("Visalizar lista de candidatos:"):
            comload = data2.loc[data2['Comarca'] == opcoes_comarca]
            st.write(comload)
            st.write(f"{comload['CNPJ/CPF Base'].count()} ocorrências")

        st.subheader('2) Selecione quem analisar:')
        st.write(f"Comarca: {opcoes_comarca}")

        comload_proin = data2['Razão Social'].loc[data2['Comarca'] == opcoes_comarca].to_list()
        # st.write(comload_proin)
        selecionados_ = st.selectbox('Digite a Razão Social ou CNPJ:', comload_proin)
        selected_rows = data2.loc[data2["Razão Social"] == selecionados_]
        st.write('Razão Social Selecionada:', selected_rows)

    if opcoes_nucleos != 'PROIN - Procuradoria do Interior':
        comarcas_PROFIS = st.selectbox("Selecione sua comarca de atuação",
                                       options=comarcas)

        st.subheader("1) Dados Candidatos")

        if st.checkbox("Visalizar lista de candidatos:"):
            candidatos_n_proin = df.loc[df['Comarca'] == comarcas_PROFIS]
            st.write(candidatos_n_proin)
            st.write(f"{candidatos_n_proin['CNPJ/CPF Base'].count()} ocorrências")

        st.subheader('2) Selecione quem analisar:')
        st.write(f"Comarca: {comarcas_PROFIS}")

        comload_proin = df['Razão Social'].loc[df['Comarca'] == comarcas_PROFIS].to_list()
        selecionados_ = st.selectbox('Digite a Razão Social ou CNPJ:', comload_proin)
        selected_rows = df.loc[df["Razão Social"] == selecionados_]
        st.write('Razão Social Selecionada:', selected_rows)
        st.write("Dios mio!")


#def quest():
    # PERGUNTAS
with st.form(key='questionario'):
    st.write('### 3) Pontue as razões da sua avaliação')
    resp_01 = ["Sim", "Não"]
    st.radio(
        'Há dificuldade de localização do devedor para citação (de preferência, usar processos mais recentes como referência)?',
        resp_01)

    resp_02 = ["Sim", "Não"]
    q01 = st.empty()
    q01.radio('No geral, o devedor apresenta garantia nas execuções (independente do tipo)?', resp_02, 0)

    resp_03 = ["Sim", "Não"]
    st.radio(
        'Caso POSITIVA a resposta anterior, a garantia apresentada nas execuções é boa(dinheiro, fiança ou seguro garantia)?',
        resp_01)

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
    st.write(
        'Atribua um score para sua percepção para a qualificação do devedor, sendo 1 um score muito baixo, e 5 muito alto')
    score_aderencia = st.slider(label='Socre Aderência:', min_value=0, max_value=5, value=0, step=1,
                                format='%f')

    submeter = st.form_submit_button("Submeter Avaliação")
    #resultados = pd.read_csv('dfs/resultados.csv')

    if submeter:

        dados_resultados = {
            'sessao': [score_aderencia]}
        df_r = pd.DataFrame(dados_resultados)
        df_r.to_csv('dfs/resultados.csv', mode="a", index=False, header=False)

    st.markdown("""
    [ver minhas avaliações](#)
    """)


opcoes = ["Razão Social", "CNPJ"]

# select_razao = st.selectbox('Digite a Razão Social ou CNPJ:', data2["Razão Social"], index=0)
# selected_rows = data2.loc[data2["Razão Social"] == select_razao]

#####################
# SIDE BAR

with st.sidebar:
    st.info(
        "🎈 **NOVIDADE:** Você agora deve escolher que quais núcleos você faz parte, antes de realizar sua avaliação..")

    st.header('Passos para sua Avaliação:')

    st.markdown("""
        - Para fazer sua avaliação identifique as informações em documentos, autos do processo, e/ou em sistemas (ex. PGE.NET, Sigat, etc.) 
        - Na coluna principal, marque as respostas e faça observações de sua avaliação (se for o caso)
        - Atribua um score de aderência a uma qualificação do devedor, de 1 a 5, sendo 1 muito baixo e muito alto.


        [ver minhas avaliações](#)
    """)

def main():
    st.title("Credenciais de acesso")

    menu = ["Home", "Login", "SignUp"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("Seu usuário")
        password = st.sidebar.text_input("Sua senha", type='password')

        if st.sidebar.button("Login"):
            # if password == 'xxx':

            result = login_user(username, password)
            usuario_ativo = result[0][1]
            setor = user_sector()
            st.sidebar.text(setor)

            usess = User(user_name=usuario_ativo)
            input = UserInput()
            session.add(usess)

            if result and setor == "proin":

                st.sidebar.success("Logado como {}".format(username))
                st.text(active_user())
                st.text(usuario_ativo)

                return exposicao_nucelos()#, quest()

            else:
                st.sidebar.warning("Password incorreto.")



    elif choice == "SignUp":
        st.subheader("Create new account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        new_email = st.text_input("Email")

        setores_pge = ["proin", "2", "3", "4"]
        new_sector = st.selectbox("Setor", setores_pge)

        if st.button("Criar cadastro"):
            add_userdata(new_user, new_password, new_email, new_sector)
            st.success("Password criado")
            st.info("Vá para o menu Login")


if __name__ == '__main__':
    main()
