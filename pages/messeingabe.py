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

if 'heutigerquicksec' not in st.session_state:
    st.session_state['heutigerquicksec'] = 0

st.session_state['aktuell'] = 'Dateneingabe'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])

def callback_calcfromsec():
    # Update the quickproz and inr variables based on the new value of quicksec
    global heutigerquickproz, inr
    heutigerquicksec = st.session_state['heutigerquicksec']
    heutigerquickproz = (st.session_state['current_ref']/heutigerquicksec)*100
    inr = (heutigerquicksec/st.session_state['current_ref'])**st.session_state['current_isi']
    # Update the value of the quickproz and inr inputs
    st.session_state.heutigerquickproz = heutigerquickproz
    st.session_state.heutigerinr = inr

def callback_calc2frominr():
    # Update the quickproz and inr variables based on the new value of quicksec
    global heutigerquickproz, heutigerquicksec
    inr = st.session_state['heutigerinr']
    heutigerquicksec = st.session_state['current_ref']*(inr)**(1/st.session_state['current_isi'])
    heutigerquickproz = (st.session_state['current_ref']/heutigerquicksec)*100
    # Update the value of the quickproz and inr inputs
    st.session_state.heutigerquickproz = heutigerquickproz
    st.session_state.heutigerquicksec = heutigerquicksec

if st.session_state['loginstatus'] != False:
    if st.session_state['medikament'] == True:
        conn = mysql.connector.connect(**connex())
        cursor = conn.cursor()
        cursor.execute('SELECT `device_name`,`device_nr` FROM `sql7710143`.`devices`')
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
        cursor.execute(f'SELECT `lot_numbers`.`lotnr`,`lot_numbers`.`expiry`,`lot_numbers`.`refquick`,`lot_numbers`.`isi` FROM `sql7710143`.`lot_numbers` JOIN `lot_data` ON `lot_data`.`new_lot` = `lot_numbers`.`id` WHERE `lot_data`.`user` = %s ORDER BY `lot_data`.`updated` DESC LIMIT 1',(user,))
        rows = cursor.fetchone()
        current_lot = rows[0]
        expiry = rows[1]
        current_ref = rows[2]
        current_isi = rows[3]
        if 'current_ref' not in st.session_state:
                    st.session_state['current_ref'] = current_ref
        if 'current_isi' not in st.session_state:
                    st.session_state['current_isi'] = current_isi
        conn.close()
        if is_expired(str(expiry)):
            st.warning('Ihre aktuelles Reagenz hat das Verfalldatum überschritten!')
        else:
            with st.expander(label='aktuelle Messumgebung (Gerät/LOT-NR. des Reagenz)',expanded=False):
                st.subheader('aktuelle Messumgebung')
                st.text(mydev)
                st.text(current_lot)
            with st.expander(label='Dateneingabe',expanded=False):
                st.subheader('Quick-Eingabe (INR-Zielwert-Eingabe)')
                heutigerquicksec = st.number_input(label = "errechneter Quick-Messwert in Sekunden", min_value=0, max_value=100, key='heutigerquicksec', step=1,disabled=True)
                heutigerquickproz = st.number_input(label = "errechneter Quick-Messwert in Prozent", key='heutigerquickproz', min_value=0.0, max_value=130.0, step=0.1,disabled=True)
                inr = st.number_input(label = "INR-Zielwert", min_value=0.00, key='heutigerinr', max_value=20.00, step=0.01, on_change=callback_calc2frominr)
                datum = st.date_input('Zeitpunkt der Messung',format='DD/MM/YYYY')
                abspeichern = st.button('Quick jetzt abspeichern')
                if abspeichern:
                    if futuredate(datum) == False:
                        if not quick_empty(st.session_state['loggedinuserid'],datum):
                            quick_eintrag(heutigerquickproz,inr,datum)
                            time.sleep(3)
                            st.rerun()
                        else:
                            datum1 = datum.strftime('%d-%m-%Y')
                            st.info(f"Am {datum1} existiert bereits eine eingetragene Messung.")
                    else:
                        st.info('Sie versuchen den Messwert an einem zukünftigen Datum abzuspeichern!')
    else:
        st.text('Noch kein Medikament erfasst!')
else:
    st.switch_page('main.py')