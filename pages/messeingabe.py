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

    if st.session_state['medikament'] == True:
        with st.expander(label='aktuelle Messumgebung (Gerät/LOT-NR. des Reagenz)',expanded=False):
            st.subheader('aktuelle Messumgebung')
            st.text(mydev)
            lot = st.selectbox(label='aktuelle LOT',options=['o1','o1','o3'])
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