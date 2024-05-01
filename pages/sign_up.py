import streamlit as st
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *
from datetime import datetime

medi_liste = {'Phenprocoumon (Marcoumar®) (CH)':1,'Warfarin (Coumadin®) (USA)':2,'(Sintrom®, Sintrom® mitis) (CH)':3}

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if 'einloggen' not in st.session_state:
    st.session_state['einloggen'] = False

if 'registrieren' not in st.session_state:
    st.session_state['registrieren'] = False

if 'medikament' not in st.session_state:
    st.session_state['medikament'] = False

st.session_state['aktuell'] = 'Meine Daten'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])

if st.session_state['loginstatus'] == False:
    if st.session_state['einloggen'] == False and st.session_state['registrieren'] == True:
        with st.sidebar.form(key='chooselog',border=True):
            if st.form_submit_button(label='Fortfahren zum Einloggen'):
                proceed_login()
    elif st.session_state['einloggen'] == True and st.session_state['registrieren'] == False:
        with st.sidebar.form(key='choosereg',border=True):
            if st.form_submit_button(label='Fortfahren zum Registrieren'):
                proceed_register()
    else:
        with st.sidebar.form(key='chooselog',border=True):
            if st.form_submit_button(label='Fortfahren zum Einloggen'):
                proceed_login()
        with st.sidebar.form(key='choosereg',border=True):
            if st.form_submit_button(label='Fortfahren zum Registrieren'):
                proceed_register()

    if st.session_state['einloggen'] == True:
        with st.sidebar.form(key='login',clear_on_submit=True,border=True):
            st.subheader('Login')
            login_username = st.text_input(label='Username ')
            login_password = st.text_input(label='Passwort ', type='password')
            st.form_submit_button(on_click=login(login_username,login_password),label='Einloggen')
    elif st.session_state['registrieren'] == True:
         with st.sidebar.form(key='register',clear_on_submit=True,border=True):
            st.subheader('Registrierung')
            username = st.text_input(label='Username', key='username')
            vorname = st.text_input(label='Vorname', key='vorname')
            nachname = st.text_input(label='Nachname', key='nachname')
            password = st.text_input(label='Passwort',type='password',key='pw')
            geburtsdatum = st.date_input(label='Geburtsdatum',format='DD/MM/YYYY')
            med = st.selectbox(label='Medikament',options=list(medi_liste.keys()),placeholder='Wählen Sie Ihr derzeitiges Medikament aus!')
            mednr = medi_liste[med]
            registerdate = datetime.today()
            st.form_submit_button(label='Registrieren',on_click=register(username,vorname,nachname,password,geburtsdatum,registerdate,mednr))
else:
    meine_userdaten(st.session_state['loggedinuserid'])
