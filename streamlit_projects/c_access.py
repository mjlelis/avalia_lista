import pandas as pd
import streamlit as st
import sqlite3
import sqlalchemy

# Criando DB

conn = sqlite3.connect('data.db')
c = conn.cursor()



def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username, password) VALUEs (?,?)', (username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def ver_usuarios():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
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
            create_usertable()
            result = login_user(username, password)
            if result:
                st.sidebar.success("Logado como {}".format(username))
                task = st.selectbox("Task", ["Profiles"])
                if task == "Profiles":
                    st.subheader('User Profiles')
                    user_result = ver_usuarios()
                    clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
            else:
                st.sidebar.warning("Password incorreto.")



    elif choice == "SignUp":
        st.subheader("Create new account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Criar cadastro"):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("Password criado")
            st.info("Vá para o menu Login")


if __name__ == '__main__':
    main()