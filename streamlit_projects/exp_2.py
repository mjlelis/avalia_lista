import pandas as pd
import streamlit as st
import sqlite3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, insert, select, and_
from login_orm import User

# Criando DB


engine = create_engine('sqlite:///reg_db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

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
    return data

def user_sector():
    stmt = select([User])
    stmt = stmt.where(User.user_sector == "proin")
    setor = c.execute(stmt).fetchall()
    for resultado in setor:
        return resultado.user_sector

def ver_usuarios():
    usuarios = select([User])
    data = c.execute(usuarios).fetchall()
    return data


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
            setor = user_sector()
            st.sidebar.text(setor)
            if result and setor=="proin":
                st.sidebar.success("Logado como {}".format(username))
                task = st.selectbox("Task", ["Profiles"])

                if task == "Profiles":
                    st.subheader('User Profiles')
                    user_result = ver_usuarios()
                    clean_db = pd.DataFrame(user_result, columns=["user_name", "user_pass", "user_email", "id"])
            else:
                st.sidebar.warning("Password incorreto.")



    elif choice == "SignUp":
        st.subheader("Create new account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        new_email = st.text_input("Email")

        setores_pge = ["1", "2", "3", "4"]
        new_sector = st.selectbox("Setor", setores_pge)

        if st.button("Criar cadastro"):
            add_userdata(new_user, new_password, new_email, new_sector)
            st.success("Password criado")
            st.info("Vá para o menu Login")


if __name__ == '__main__':
    main()
