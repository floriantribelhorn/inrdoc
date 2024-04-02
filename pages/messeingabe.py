import streamlit as st
from functions.database_new import *
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

st.session_state['aktuell'] = 'Dateneingabe'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])

if st.session_state['loginstatus'] != False:
    with st.container(border=True):
        st.subheader('Quick-Eingabe')
        heutigerquick = st.number_input(label = "Quick-Messwert", min_value=0, max_value=100, step=1)
        datum = st.date_input('Zeitpunkt der Messung',format='DD/MM/YYYY')
        abspeichern = st.button('Quick jetzt abspeichern')
        if abspeichern:
            if not quick_empty(st.session_state['loggedinuserid'],datum):
                quick_eintrag(heutigerquick,datum)
            else:
                datum1 = datum.strftime('%d-%m-%Y')
                st.info(f"Am {datum1} existiert bereits eine eingetragene Messung.")
