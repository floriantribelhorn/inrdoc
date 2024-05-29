import streamlit as st
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *
from functions.cnx import *
import time

#Datenbank-Abfrage, ob eingeloggter user bereits ein Gerät erfasst hat (bei Neuregistration nie), Gerätenummer wird in Liste rows abgespeichert
conn = mysql.connector.connect(**connex())
cursor = conn.cursor()
cursor.execute(f'SELECT `device_data`.`new_device`  FROM `device_data` WHERE `user` = %s ORDER BY `device_data`.`updated` DESC LIMIT 1''',(st.session_state['loggedinuserid'],))
rows = cursor.fetchone()
if rows:
    current_device = rows[0]
conn.close()

#Schrittweise Gerät erfassen, Lot-Nr. erfassen und danach Zielwerte INR erfassen (mit Funktionen device_update2, lot_update1 und level_update)
if not rows:
    with st.container(border=True):
            st.subheader('In Ihrem Profil wurde noch kein Gerät erfasst!')
            dev = st.selectbox(label='Messgerät',options=list(device_dict.keys()),placeholder='Wählen Sie Ihr Messgerät aus!')
            btn = st.button(label='Abspeichern')
            if btn:
                device = device_dict[dev]
                device_update2(device)
else:
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute(f'SELECT `device_data`.`new_device`, `ld`.`new_lot` FROM `device_data` JOIN (SELECT `user`, `new_lot` FROM `lot_data` ld WHERE (`user`, `updated`) IN (SELECT `user`, MAX(`updated`) FROM `lot_data` GROUP BY `user`)) `ld` ON `device_data`.`user` = `ld`.`user` WHERE `device_data`.`user` = %s ORDER BY `device_data`.`updated` DESC LIMIT 1''',(st.session_state['loggedinuserid'],))
    rows2 = cursor.fetchall()
    if rows2:
        current_device = rows2[0][0]
        current_lot = rows2[0][1]
    conn.close()

    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute(f'SELECT `device_data`.`new_device`, `ld`.`new_lot`, `targetlevel`.* FROM `device_data` JOIN ( SELECT `user`, `new_lot` FROM `lot_data` ORDER BY `updated` DESC ) `ld` ON `device_data`.`user` = `ld`.`user` JOIN `targetlevel` ON `device_data`.`user` = `targetlevel`.`user` WHERE `device_data`.`user` = %s ORDER BY `device_data`.`updated` DESC LIMIT 1''',(st.session_state['loggedinuserid'],))
    rows3 = cursor.fetchall()
    if rows3:
        targetlevel = rows3[0][5]
    conn.close()
    
    if not rows2:
        conn = mysql.connector.connect(**connex())
        cursor = conn.cursor()
        cursor.execute('SELECT `id`,`lotnr`,`device` FROM `sql7710143`.`lot_numbers`')
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

        with st.container(border=True):
            with st.form(key='lotupdate',clear_on_submit=True,border=True):
                st.subheader('In Ihrem Profil wurde noch keine Lot-Nr. des Reagenz erfasst!')
                if current_device == 1:
                    lot = st.selectbox(label='LOT-Nr.',options=list(dict1.values()),placeholder='Wählen Sie Ihre aktuelle LOT-Nr. aus!')
                elif current_device == 2:  
                    lot = st.selectbox(label='LOT-Nr.',options=list(dict2.values()),placeholder='Wählen Sie Ihre aktuelle LOT-Nr. aus!')
                else:
                    lot = st.selectbox(label='LOT-Nr.',options=list(dict3.values()),placeholder='Wählen Sie Ihre aktuelle LOT-Nr. aus!')
                st.form_submit_button(label='Abspeichern',on_click=lot_update1, args=(lot,))
    elif not rows3:
        with st.container(border=True):
            st.subheader('Erfassen Sie Ihren INR-Zielwert!')
            levelh = st.number_input(label='Oberer INR-Wert',min_value=0.0,max_value=10.0,step=0.1,value=10.0)
            levell = st.number_input(label='Unterer INR-Wert',min_value=0.0,max_value=10.0,step=0.1,value=0.0)
            aktualisieren = st.button(label='Aktualisieren')
            if aktualisieren:
                level_update(levelh,levell)
    else:
        conn = mysql.connector.connect(**connex())
        cursor = conn.cursor()
        cursor.execute('SELECT `id`,`lotnr`,`device` FROM `sql7710143`.`lot_numbers`')
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

        with st.container(border=True):
                st.subheader('LOT-NR. aktualisieren!')
                if current_device == 1:
                    lot = st.selectbox(label='LOT-Nr.',options=list(dict1.values()),placeholder='Wählen Sie Ihre aktuelle LOT-Nr. aus!')
                elif current_device == 2:  
                    lot = st.selectbox(label='LOT-Nr.',options=list(dict2.values()),placeholder='Wählen Sie Ihre aktuelle LOT-Nr. aus!')
                else:
                    lot = st.selectbox(label='LOT-Nr.',options=list(dict3.values()),placeholder='Wählen Sie Ihre aktuelle LOT-Nr. aus!')
                click = st.button(label='Abspeichern')
                if click:
                    lot_update2(lot)
                    time.sleep(5)
                    st.switch_page('pages/sign_up.py')
