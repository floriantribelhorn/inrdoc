import streamlit as st
import mysql.connector
from functions.utilities import *

medi_liste = {'Phenprocoumon (Marcoumar®) (CH)':1,'Warfarin (Coumadin®) (USA)':2,'(Sintrom®, Sintrom® mitis) (CH)':3}

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

def register(username,vorname,nachname,password,geburtsdatum,registerdate,med):
    if empty_check(username,vorname,nachname,password,geburtsdatum,registerdate) == True:
        username_check(username)
        if st.session_state['usernameavailable'] == True:
            user_anlegen(username,password,vorname,nachname,geburtsdatum,registerdate,med)
            st.success('Registrierung erfolgreich, nun können sie sich einloggen',icon="🤖")       
    else:
        st.info('Füllen sie alle Felder aus')

def username_check(username):
    if 'usernameavailable' not in st.session_state:
        st.session_state['usernameavailable'] = False
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT `username` FROM `freedb_inrdoc`.`user_data` WHERE username = %s',(username,))
    rows = cursor.fetchall()
    
    if not rows:
        st.session_state['usernameavailable'] = True
    else:
        st.error('Dieser Username ist schon vergeben!')
        st.session_state['usernameavailable'] = False
    
    conn.commit()
    conn.close()

def user_anlegen(username,password,vorname,nachname,geburtsdatum,registerdate,med):
    passwordcheck = md5sum(password)
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO `freedb_inrdoc`.`user_data` (username, password, vorname, nachname, register_date, birthdate, med)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (username, passwordcheck, vorname, nachname, registerdate, geburtsdatum,med))
    conn.commit()
    conn.close()
    
def user_einloggen(username, password):
    pw = md5sum(password)
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()

    cursor.execute('SELECT `id`,`username`, `password`,`vorname`, `med` FROM `freedb_inrdoc`.`user_data` WHERE username = %s', (username,))
    rows = cursor.fetchall()

    if len(rows) == 1:
        userid, uname, pw1, vname, medi = rows[0]
        if uname == username and pw1 == pw:
            st.success('eingeloggt',icon='🔒')
            st.session_state['loginstatus'] = True
            st.session_state['loggedinuser'] = vname
            st.session_state['loggedinuserid'] = userid
            if medi != '0':
                st.session_state['medikament'] = True
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

def update_username(id, username):
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT `username` FROM `freedb_inrdoc`.`user_data` WHERE `id` = %s', (id,))
    rows = cursor.fetchall()
    if 'changedname' not in st.session_state:
        st.session_state['changedname'] = False
        st.session_state['changedname'] = rows[0][0]
    conn.commit()
    conn.close()
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('UPDATE `freedb_inrdoc`.`user_data` SET `username` = %s WHERE `id` = %s', (username, id,))
    num_rows_updated = cursor.rowcount
    cn = st.session_state['changedname']
    if num_rows_updated != '':
        st.success(f'Username von {cn} zu {username} geändert.')
    conn.commit()
    conn.close()

def name_update(id,vorname,nachname):
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT `vorname`,`nachname` FROM `freedb_inrdoc`.`user_data` WHERE `id` = %s', (id,))
    rows = cursor.fetchall()
    vorname1 = rows[0][0]
    nachname1 = rows[0][1]
    conn.commit()
    conn.close()
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('UPDATE `freedb_inrdoc`.`user_data` SET `vorname` = %s,`nachname` = %s WHERE `id` = %s', (vorname,nachname, id,))
    num_rows_updated = cursor.rowcount
    if num_rows_updated != '':
        if vorname1 == vorname and nachname1 == nachname:
            st.info('Alles beim alten, nichts wurde geändert')
        elif vorname1 != vorname and nachname1 == nachname:
            st.info(f'Vorname von {vorname1} zu {vorname} geändert.')
            st.session_state['loggedinuser'] = vorname
        elif vorname1 == vorname and nachname1 != nachname:
            st.info(f'Nachname von {nachname1} zu {nachname} geändert.')
        else:
            st.info(f'Vorname von {vorname1} zu {vorname} und Nachname von {nachname1} zu {nachname} geändert.')
    conn.commit()
    conn.close()

def birthdate_update(id,bd):
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT `birthdate` FROM `freedb_inrdoc`.`user_data` WHERE `id` = %s', (id,))
    rows = cursor.fetchall()
    altbd = rows[0][0]
    conn.commit()
    conn.close()
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('UPDATE `freedb_inrdoc`.`user_data` SET `birthdate` = %s WHERE `id` = %s', (bd, id,))
    num_rows_updated = cursor.rowcount
    if num_rows_updated != '':
        st.info(f'Altes Geburtsdatum: {altbd}, neues Geburtsdatum: {bd}')
    else:
        st.info('Alles beim Alten!')
    conn.commit()
    conn.close()

def med_updater(user,medi):
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT `med` FROM `freedb_inrdoc`.`user_data` WHERE `id` = %s', (user,))
    rows = cursor.fetchall()
    altmed = rows[0][0]
    conn.commit()
    conn.close()
    if medi == 'Phenprocoumon (Marcoumar®) (CH)':
        um = 1
    elif medi == 'Warfarin (Coumadin®) (USA)':
        um = 2
    elif medi == '(Sintrom®, Sintrom® mitis) (CH)':
        um = 3
    else:
        um = 0
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('UPDATE `freedb_inrdoc`.`user_data` SET `med` = %s WHERE `id` = %s', (um, user,))
    num_rows_updated = cursor.rowcount
    if num_rows_updated != '':
        st.info(f'Altes Medikament: {altmed}, neues Medikament: {medi}')
    else:
        st.info('Alles beim Alten!')
    conn.commit()
    conn.close()

def meine_userdaten(user):
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM `freedb_inrdoc`.`user_data` WHERE id = %s', (user,))
    rows = cursor.fetchall()

    with st.container(border=True):
        st.subheader('Meine Profildaten')
        for row in rows:
            id, username, first_name, last_name, register_date, birthdate, password, med = row
            un = st.text_input(label='Username', value=username, key='uname')
            vn = st.text_input(label='Vorname', value=first_name)
            sn = st.text_input(label='Nachname', value=last_name)
            bd = st.date_input(label='Geburtsdatum', format='DD/MM/YYYY', value=birthdate)
            medi = st.selectbox(label='Medikament',options=medi_liste,index=med-1)
            st.write(f'Registriert am: {register_date.strftime("%d/%m/%Y")}')
        namen_update = st.button(label='Namen ändern')
        username_update = st.button(label='Username ändern')
        gebdat_update = st.button(label='Geburtsdatum ändern')
        med_update = st.button(label='Medikament ändern')
        st.button(label='Passwort ändern')

        if username_update:
            username_check(un)
            if st.session_state['usernameavailable'] == True:
                update_username(user,un)
        if namen_update:
            name_update(id,vn,sn)
        if gebdat_update:
            birthdate_update(user,bd)
        if med_update:
            med_updater(user,medi)