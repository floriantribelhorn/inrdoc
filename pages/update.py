import streamlit as st
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *
from functions.cnx import *

conn = mysql.connector.connect(**connex())
cursor = conn.cursor()
cursor.execute('SELECT `device_name`,`device_nr` FROM `freedb_inrdoc`.`devices`')
rows = cursor.fetchall()
device_dict = {}
for name, nr in rows:
    device_dict[name] = nr
conn.commit()
conn.close()

with st.container(border=True):
    with st.form(key='deviceupdate',clear_on_submit=True,border=True):
        st.subheader('In Ihrem Profil wurde noch kein Messgerät erfasst!')
        dev = st.selectbox(label='Medikament',options=list(device_dict.keys()),placeholder='Wählen Sie Ihr derzeitiges Messgerät aus!')
        device = device_dict[dev]
        st.form_submit_button(label='Abspeichern',on_click=device_update, args=(device,))
if st.button('Weiterfahren'):
    st.switch_page('main.py')