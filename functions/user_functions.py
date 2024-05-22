import streamlit as st
import mysql.connector
from functions.utilities import *
from functions.cnx import *
from datetime import datetime

def login(username,password):
    if empty_check2(username,password):
        user_einloggen(username,password)
    else:
        st.info('Füllen Sie beide Felder aus!')

def register(username,vorname,nachname,password,password_repeat,geburtsdatum,registerdate,med):
    if empty_check3(username,vorname,nachname,password,password_repeat,geburtsdatum,registerdate) == True:
        if password == password_repeat:
            username_check(username)
            if st.session_state['usernameavailable'] == True:
                user_anlegen(username,password,vorname,nachname,geburtsdatum,registerdate,med)
                st.success('Registrierung erfolgreich, nun können sie sich einloggen',icon="🤖")   
        else:
            st.warning('Passwörter stimmen nicht überein🔥')    
    else:
        st.info('Füllen sie alle Felder aus')

def username_check(username):
    if 'usernameavailable' not in st.session_state:
        st.session_state['usernameavailable'] = False
    
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('SELECT `username` FROM `freedb_inrdoc`.`user_data` WHERE username = %s',(username,))
    rows = cursor.fetchall()
    
    if not rows:
        st.session_state['usernameavailable'] = True
    else:
        st.error('Dieser Username ist schon vergeben!')
        st.session_state['usernameavailable'] = False
    conn.close()

def lot_check(user):
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('SELECT `new_lot` FROM `freedb_inrdoc`.`lot_data` WHERE user = %s ORDER BY updated DESC LIMIT 1',(user,))
    rows = cursor.fetchone()
    conn.close()
    if not rows:
        return False
    else:
        return rows[0]

def user_anlegen(username,password,vorname,nachname,geburtsdatum,registerdate,med):
    passwordcheck = md5sum(password)
    
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO `freedb_inrdoc`.`user_data` (username, password, vorname, nachname, register_date, birthdate, med)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (username, passwordcheck, vorname, nachname, registerdate, geburtsdatum,med))
    conn.commit()
    conn.close()
    
def user_einloggen(username, password):
    pw = md5sum(password)
    
    conn = mysql.connector.connect(**connex())
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
                if lot_check(userid) == False:
                    st.switch_page('pages/update.py')
                else:
                    st.switch_page('main.py')
        elif uname == username and pw1 != pw:
            st.warning('falsches Passwort', icon="⚠️")    
    else:
        st.warning('nicht existierender Benutzername',icon="⚠️")

    conn.commit()
    conn.close()

def user_data_check():
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM `freedb_inrdoc`.`user_data`')
    rows = cursor.fetchall()

    for row in rows:
        st.table(row)
    conn.close()

def update_username(id, username):
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('SELECT `username` FROM `freedb_inrdoc`.`user_data` WHERE `id` = %s', (id,))
    rows = cursor.fetchall()
    if 'changedname' not in st.session_state:
        st.session_state['changedname'] = False
        st.session_state['changedname'] = rows[0][0]
    conn.commit()
    conn.close()
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('UPDATE `freedb_inrdoc`.`user_data` SET `username` = %s WHERE `id` = %s', (username, id,))
    num_rows_updated = cursor.rowcount
    cn = st.session_state['changedname']
    if num_rows_updated != '':
        st.success(f'Username von {cn} zu {username} geändert.')
    conn.commit()
    conn.close()

def name_update(id,vorname,nachname):
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('SELECT `vorname`,`nachname` FROM `freedb_inrdoc`.`user_data` WHERE `id` = %s', (id,))
    rows = cursor.fetchall()
    vorname1 = rows[0][0]
    nachname1 = rows[0][1]
    conn.commit()
    conn.close()
    conn = mysql.connector.connect(**connex())
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
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('SELECT `birthdate` FROM `freedb_inrdoc`.`user_data` WHERE `id` = %s', (id,))
    rows = cursor.fetchall()
    altbd = rows[0][0]
    conn.commit()
    conn.close()
    conn = mysql.connector.connect(**connex())
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
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('SELECT `med` FROM `freedb_inrdoc`.`user_data` WHERE `id` = %s', (user,))
    rows = cursor.fetchall()
    altmed = rows[0][0]
    for key, value in drugs_dict.items():
        if value == altmed:
            altmed = key
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
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('UPDATE `freedb_inrdoc`.`user_data` SET `med` = %s WHERE `id` = %s', (um, user,))
    num_rows_updated = cursor.rowcount
    if num_rows_updated != '':
        st.info(f'Altes Medikament: {altmed}, neues Medikament: {medi}')
    else:
        st.info('Alles beim Alten!')
    conn.commit()
    conn.close()

def lot_update1(lot):
    user = st.session_state['loggedinuserid']
    date = datetime.today().date()
    time = datetime.now().time()
    new_datetime = datetime.combine(date, time)
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('''SELECT `id` FROM `freedb_inrdoc`.`lot_numbers` WHERE `lotnr` = %s ''',(lot,))
    row = cursor.fetchone()
    lot_id = row[0]
    conn.close()
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO `freedb_inrdoc`.`lot_data` (new_lot, updated, user) VALUES  (%s,%s,%s) ''', (lot_id, new_datetime, user))
    num_rows_updated = cursor.rowcount
    if num_rows_updated:
        st.success('LOT EINGETRAGEN')
    else:
        st.info('Hat nicht geklappt!')
    conn.commit()
    conn.close()

def lot_update2(lot):
    user = st.session_state['loggedinuserid']
    date = datetime.today().date()
    time = datetime.now().time()
    new_datetime = datetime.combine(date, time)
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('''SELECT `id` FROM `freedb_inrdoc`.`lot_numbers` WHERE `lotnr` = %s ''',(lot,))
    row = cursor.fetchone()
    lot_id = row[0]
    conn.close()
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('''SELECT `new_lot` FROM `freedb_inrdoc`.`lot_data` WHERE `user` = %s ORDER BY `updated` DESC LIMIT 1''',(user,))
    row = cursor.fetchone()
    old_id = row[0]
    conn.close()
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO `freedb_inrdoc`.`lot_data` (old_lot, new_lot, updated, user) VALUES  (%s,%s,%s,%s) ''', (old_id,lot_id, new_datetime, user))
    num_rows_updated = cursor.rowcount
    if num_rows_updated:
        st.success('LOT aktualisiert')
    else:
        st.info('Hat nicht geklappt!')
    conn.commit()
    conn.close()

def device_update2(device):
    user = st.session_state['loggedinuserid']
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('''SELECT `device_data`.`new_device`  FROM `device_data` WHERE `user` = %s ORDER BY `device_data`.`updated` DESC LIMIT 1''',(user,))
    row = cursor.fetchone()
    if row:
        olddev = row[0]
        olddev2 = keys[olddev-1]
    else:
        olddev = ''
        olddev2 = 'kein vorheriges Gerät'
    keys = list(device_dict.keys())
    device2 = device_dict[device]
    user = st.session_state['loggedinuserid']
    date = datetime.today().date()
    time = datetime.now().time()
    new_datetime = datetime.combine(date, time)
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO `freedb_inrdoc`.`device_data`  (old_device, new_device, user, updated) VALUES  (%s,%s,%s,%s) ''', (olddev,device2, user, new_datetime))
    num_rows_updated = cursor.rowcount
    if num_rows_updated:
        st.success(f'Messgerät aktualisiert von {olddev2} zu {device}!"')
    else:
        st.info('Hat nicht geklappt!')
    conn.commit()
    conn.close()

def meine_userdaten(user):
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('SELECT `id`,`lotnr`,`device` FROM `freedb_inrdoc`.`lot_numbers`')
    rows = cursor.fetchall()
    dict1 = {}
    dict2 = {}
    dict3 = {}
    for id, lot_nr, device in rows:
        if device == 1:
            dict1[id] = lot_nr
        elif device == 2:
            dict2[id] = lot_nr
        else:
            dict3[id] = lot_nr
    conn.close()
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute(f"""SELECT `user_data`.`id`, `user_data`.`username`, `user_data`.`vorname`, `user_data`.`nachname`, `user_data`.`register_date`, `user_data`.`birthdate`, `user_data`.`password`, `user_data`.`med`, `device_data`.`old_device`, `device_data`.`new_device`, `device_data`.`updated`, `lot_data`.`new_lot`, `lot_data`.`updated`, `lot_numbers`.`device`
FROM `user_data`
JOIN `device_data` ON `user_data`.`id` = `device_data`.`user`
JOIN `lot_data` ON `user_data`.`id` = `lot_data`.`user`
JOIN `lot_numbers` ON `lot_data`.`new_lot` = `lot_numbers`.`id`
JOIN (
    SELECT `user`, MAX(`updated`) AS `max_updated`
    FROM `device_data`
    WHERE `user` = %s
    GROUP BY `user`
) AS `latest_device` ON `device_data`.`user` = `latest_device`.`user` AND `device_data`.`updated` = `latest_device`.`max_updated`
WHERE `user_data`.`id` = %s
ORDER BY `device_data`.`updated` DESC, `lot_data`.`updated` DESC
LIMIT 1""",(user,user,))
    rows = cursor.fetchall()
    conn.close()
    with st.expander(label='Meine Profildaten',expanded=False):
        st.subheader('Meine Profildaten')
        for row in rows:
            co1, co2, co3, co4 = st.columns(4)
            id, username, first_name, last_name, register_date, birthdate, password, med, old_device, new_device, updated1, new_lot, updated2, agreement = row
            with co1:
                un = st.text_input(label='Username', value=username, key='uname')
            with co2:
                vn = st.text_input(label='Vorname', value=first_name)
            with co3:
                sn = st.text_input(label='Nachname', value=last_name)
            with co4:
                bd = st.date_input(label='Geburtsdatum', format='DD/MM/YYYY', value=birthdate)
            st.write(f'Registriert am: {register_date.strftime("%d/%m/%Y")}')
    with st.expander(label='Medikament',expanded=False):
            st.subheader('Mein Medikament')  
            medi = st.selectbox(label='Medikament',options=drugs_dict,index=med-1,label_visibility='collapsed')
    with st.expander(label='Messgerät + LOT-NR.',expanded=False):
            st.subheader('Mein Messgerät und aktuelle LOT-Nr. des Reagenz')      
            device = st.selectbox(label='device',options=device_dict,index=new_device-1,label_visibility='collapsed')
            if new_device == agreement:
                if new_device == 1:
                    lot = st.selectbox(label='aktuelle LOT-Nr.', options=list(dict1.values()),index=new_lot-1)
                elif new_device == 2:
                    lot = st.selectbox(label='aktuelle LOT-Nr.', options=list(dict2.values()),index=new_lot-4)
                else:
                    lot = st.selectbox(label='aktuelle LOT-Nr.', options=list(dict3.values()),index=new_lot-7)
            else:
                dicts = {
                    1: dict1,
                    2: dict2,
                    3: dict3
                }
                dict4 = dicts[new_device]
                lot = st.selectbox(label='bitte LOT-NR. zum passenden Gerät auswählen', options=list(dict4.values()))
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        username_update = st.button(label='Username ändern')
    with col2:
        namen_update = st.button(label='Namen ändern')
    with col3:
        gebdat_update = st.button(label='Geburtsdatum ändern')
    with col4:
        med_update = st.button(label='Medikament ändern')
    with col5:
        dev_update = st.button(label='Messgerät ändern')
    with col6:
        lot_update = st.button(label='LOT-NR. aktualisieren')
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
    if dev_update:
        device_update2(device)
    if lot_update:
        lot_update2(lot)