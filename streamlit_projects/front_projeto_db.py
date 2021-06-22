from sqlalchemy.orm import sessionmaker
from project_orm import UserInput,Prediction
from sqlalchemy import create_engine
import streamlit as st

engine = create_engine( 'sqlite:///prject_db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

st.title("Projeto DB users with SQL Alchemy")

username = st.sidebar.text_input("Seu usuário")
password = st.sidebar.text_input("Sua senha", type='password')

with st.form(key="questionario"):

    area = st.number_input('Enter house area in sqft',
                           max_value=10000,
                           min_value=100,
                           value=120)

    rooms = st.number_input('Enter house area in sqft',
                           max_value=100,
                           min_value=1,
                           value=1)
    age = st.number_input('Enter age of house',
                            max_value=600,
                            min_value=1,
                            value=20)
    loc_option = ["near", "far"]
    location = st.radio("O qual a localizacao", loc_option)

    submeter = st.form_submit_button("Submeter Avaliação")

    if submeter and location:
        try:
            entry = UserInput(house_area = area,
                              no_of_rooms = rooms,
                              age = age,
                              location = location)
            sess.add(entry)
            sess.commit()
            st.success("Os dados de sua avalição foram adicionados com sucesso")
        except Exception as e:
            st.error(f"Algum erro ocorreu :|{e}) ")

    if st.checkbox("view records"):
        results = sess.query(UserInput).all()
        for item in results:
            st.subheader(item.location)
            st.text(item.house_area)