import streamlit as st
import mysql.connector
from functions.utilities import *

cnxn_str = {
    'user': 'freedb_inrdocuser',
    'password': '?$R8*?pKxKvmg5X',
    'host': 'sql.freedb.tech',
    'database': 'freedb_inrdoc',
    'port': '3306',
    'auth_plugin':'mysql_native_password'
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