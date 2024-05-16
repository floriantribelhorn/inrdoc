import streamlit as st
from functions.database_new import *
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *
from functions.cnx import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if 'medikament' not in st.session_state:
    st.session_state['medikament'] = False

st.session_state['aktuell'] = 'Dateneingabe'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])

if st.session_state['loginstatus'] != False:
    if st.session_state['medikament'] == True:
        conn = mysql.connector.connect(**connex())
        cursor = conn.cursor()
        cursor.execute('SELECT `device_name`,`device_nr` FROM `freedb_inrdoc`.`devices`')
        rows = cursor.fetchall()
        device_dict = {}
        for name, nr in rows:
            device_dict[name] = nr
        conn.close()
        mydevicelist = list(device_dict.keys())
        nr = mydevice(st.session_state['loggedinuserid'])
        mydev = mydevicelist[nr-1]
        user = st.session_state['loggedinuserid']
        conn = mysql.connector.connect(**connex())
        cursor = conn.cursor()
        cursor.execute(f'SELECT `lot_numbers`.`lotnr`,`lot_numbers`.`expiry` FROM `freedb_inrdoc`.`lot_numbers` JOIN `lot_data` ON `lot_data`.`new_lot` = `lot_numbers`.`id` WHERE `lot_data`.`user` = %s ORDER BY `lot_data`.`updated` DESC LIMIT 1',(user,))
        rows = cursor.fetchone()
        current_lot = rows[0]
        expiry = rows[1]
        conn.close()
        if is_expired(str(expiry)):
            st.warning('Ihre aktuelles Reagenz hat das Verfalldatum überschritten!')
        else:
            with st.expander(label='aktuelle Messumgebung (Gerät/LOT-NR. des Reagenz)',expanded=False):
                st.subheader('aktuelle Messumgebung')
                st.text(mydev)
                st.text(current_lot)
            with st.expander(label='Dateneingabe',expanded=False):
                st.subheader('Quick-Eingabe')
                heutigerquick = st.number_input(label = "Quick-Messwert", min_value=0, max_value=130, step=1)
                datum = st.date_input('Zeitpunkt der Messung',format='DD/MM/YYYY')
                abspeichern = st.button('Quick jetzt abspeichern')
                if abspeichern:
                    if futuredate(datum) == False:
                        if not quick_empty(st.session_state['loggedinuserid'],datum):
                            quick_eintrag(heutigerquick,datum)
                        else:
                            datum1 = datum.strftime('%d-%m-%Y')
                            st.info(f"Am {datum1} existiert bereits eine eingetragene Messung.")
                    else:
                        st.info('Sie versuchen den Messwert an einem zukünftigen Datum abzuspeichern!')
    else:
        st.text('Noch kein Medikament erfasst!')
else:
    st.switch_page('main.py')