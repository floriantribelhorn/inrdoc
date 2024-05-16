import streamlit as st
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *
from functions.cnx import *
import time

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
cursor.execute(f'SELECT `device_data`.`new_device`  FROM `device_data` WHERE `user` = %s ORDER BY `device_data`.`updated` DESC LIMIT 1''',(st.session_state['loggedinuserid'],))
rows = cursor.fetchone()
if rows:
    current_device = rows[0]
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
        click = st.button(label='Weiterfahren zur App')
        if click:
            time.sleep(3)
            st.switch_page('main.py')