import streamlit as st
from functions.functions1_new import *
from functions.database_new import *
import hashlib as ha
from datetime import datetime

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if __name__ == '__main__':
    main(st.session_state['loginstatus'])

if st.session_state['loginstatus'] == False:
    with st.sidebar.container(height=280, border=True):
        st.subheader('Login')
        login_username = st.text_input(label='Username ')
        login_password = st.text_input(label='Passwort ', type='password')
        einloggen = st.button(label='Einloggen')

    if einloggen:
        if empty_check2(login_username,login_password):
            user_einloggen(login_username,login_password)
        else:
            st.write('Füllen Sie beide Felder aus!')

    with st.sidebar.container(height=530,border=True):
        st.subheader('Registrierung')
        username = st.text_input(label='Username')
        vorname = st.text_input(label='Vorname')
        nachname = st.text_input(label='Nachname')
        password = st.text_input(label='Passwort',type='password')
        geburtsdatum = st.date_input(label='Geburtsdatum')
        registerdate = datetime.today().strftime("%A, %B %d, %Y %H:%M:%S")
        abspeichern = st.button(label='Registrieren')

        if abspeichern:
            if empty_check(username,vorname,nachname,password,geburtsdatum,registerdate) == True:
                username_check(username)
                if st.session_state['usernameavailable'] == True:
                    user_anlegen(username,password,vorname,nachname,geburtsdatum,registerdate)
            else:
                st.write('Füllen sie alle Felder aus')