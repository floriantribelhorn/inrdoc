import streamlit as st
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *
from functions.cnx import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

st.session_state['aktuell'] = 'Datenüberblick'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])

if st.session_state['loginstatus'] != False:
    with st.expander(label='Zeitraum anzeigen',expanded=False):
        zeit = st.selectbox('Quick-Werte Zeitraum:', ('5 Tage','10 Tage', '30 Tage', '2 Monate','6 Monate','1 Jahr'))
        zeigen = st.button('Werte ausgeben')

    if zeigen:
        dauer = zeitraum(zeit)
        quick_data_check(st.session_state['loggedinuserid'],dauer)
else:
    st.switch_page('main.py')
