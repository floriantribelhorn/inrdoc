import streamlit as st
from functions.functions1_new import *
from functions.database_new import *
import hashlib as ha
from datetime import datetime

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if 'empty' not in st.session_state:
    st.session_state['empty'] = ""

st.session_state['aktuell'] = 'Meine Daten'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])

if st.session_state['loginstatus'] == False:
    with st.sidebar.form(key='login',clear_on_submit=True,border=True):
        st.subheader('Login')
        login_username = st.text_input(label='Username ')
        login_password = st.text_input(label='Passwort ', type='password')
        st.form_submit_button(on_click=login(login_username,login_password),label='Einloggen')
        
    with st.sidebar.form(key='register',clear_on_submit=True,border=True):
        st.subheader('Registrierung')
        username = st.text_input(label='Username', key='username')
        vorname = st.text_input(label='Vorname', key='vorname')
        nachname = st.text_input(label='Nachname', key='nachname')
        password = st.text_input(label='Passwort',type='password',key='pw')
        geburtsdatum = st.date_input(label='Geburtsdatum')
        registerdate = datetime.today().strftime("%A, %B %d, %Y %H:%M:%S")
        st.form_submit_button(label='Registrieren',on_click=register(username,vorname,nachname,password,geburtsdatum,registerdate))
else:
    with st.container(border=True):
        st.subheader('Meine Profildaten')
        st.text_input(label='Username')
        st.text_input(label='Vorname')
        st.text_input(label='Nachname')
        st.text_input(label='Passwort',type='password')
        st.date_input(label='Geburtsdatum')
