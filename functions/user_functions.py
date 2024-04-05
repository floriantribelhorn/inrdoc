import streamlit as st
import mysql.connector
from functions.utilities import *

cnxn_str = {
    'user': st.secrets.db_credentials.user,
    'password': st.secrets.db_credentials.password,
    'host': st.secrets.db_credentials.host,
    'database': st.secrets.db_credentials.database,
    'port': st.secrets.db_credentials.port,
    'auth_plugin': st.secrets.db_credentials.auth_plugin
}

def login(username,password):
    if empty_check2(username,password):
        user_einloggen(username,password)
    else:
        st.info('Füllen Sie beide Felder aus!')

def register(username,vorname,nachname,password,geburtsdatum,registerdate):
    if empty_check(username,vorname,nachname,password,geburtsdatum,registerdate) == True:
        username_check(username)
        if st.session_state['usernameavailable'] == True:
            user_anlegen(username,password,vorname,nachname,geburtsdatum,registerdate)
            st.success('Registrierung erfolgreich, nun können sie sich einloggen',icon="🤖")       
    else:
        st.info('Füllen sie alle Felder aus')

def username_check(username):
    if 'usernameavailable' not in st.session_state:
        st.session_state['usernameavailable'] = True
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT `username` FROM `freedb_inrdoc`.`user_data` WHERE username = %s',(username,))
    rows = cursor.fetchall()
    
    if not rows:
        st.session_state['usernameavailable'] = True
    else:
        st.write('Dieser Username ist schon vergeben')
        st.session_state['usernameavailable'] = False
    
    conn.commit()
    conn.close()

def user_anlegen(username,password,vorname,nachname,geburtsdatum,registerdate):
    passwordcheck = md5sum(password)
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO `freedb_inrdoc`.`user_data` (username, password, vorname, nachname, register_date, birthdate)
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (username, passwordcheck, vorname, nachname, registerdate, geburtsdatum))
    conn.commit()
    conn.close()
    
def user_einloggen(username, password):
    pw = md5sum(password)
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()

    cursor.execute('SELECT `id`,`username`, `password`,`vorname` FROM `freedb_inrdoc`.`user_data` WHERE username = %s', (username,))
    rows = cursor.fetchall()

    if len(rows) == 1:
        userid, uname, pw1, vname = rows[0]
        if uname == username and pw1 == pw:
            st.success('eingeloggt',icon='🔒')
            st.session_state['loginstatus'] = True
            st.session_state['loggedinuser'] = vname
            st.session_state['loggedinuserid'] = userid
            st.switch_page('main.py')
        elif uname == username and pw1 != pw:
            st.warning('falsches Passwort', icon="⚠️")    
    else:
        st.warning('nicht existierender Benutzername',icon="⚠️")

    conn.commit()
    conn.close()

def user_data_check():
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM `freedb_inrdoc`.`user_data`')
    rows = cursor.fetchall()

    for row in rows:
        st.table(row)

    conn.commit()
    conn.close()

def meine_userdaten11(user):
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM `freedb_inrdoc`.`user_data` WHERE id = %s', (user,))
    rows = cursor.fetchall()

    with st.container(border=True):
        st.subheader('Meine Profildaten')
        st.text_input(label='Username',value=1)
        st.text_input(label='Vorname',value=2)
        st.text_input(label='Nachname',value=3)
        st.text_input(label='Passwort',type='password',value=4)
        st.date_input(label='Geburtsdatum',format='DD/MM/YYYY',value=5)

def meine_userdaten(user):
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM `freedb_inrdoc`.`user_data` WHERE id = %s', (user,))
    rows = cursor.fetchall()

    with st.container(border=True):
        st.subheader('Meine Profildaten')
        for row in rows:
            id, username, first_name, last_name, register_date, birthdate, password = row
            st.text_input(label='Username', value=username)
            st.text_input(label='Vorname', value=first_name)
            st.text_input(label='Nachname', value=last_name)
            st.text_input(label='Passwort', type='password', value=password)
            st.date_input(label='Geburtsdatum', format='DD/MM/YYYY', value=birthdate)
            st.write(f'Registriert am: {register_date.strftime("%d/%m/%Y")}')