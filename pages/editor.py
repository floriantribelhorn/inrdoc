import streamlit as st
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *
from functions.cnx import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if 'anzeigebutton' not in st.session_state:
    st.session_state['anzeigebutton'] = False

st.session_state['aktuell'] = 'Dateneditor'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])
    if st.session_state['loginstatus'] != False:
        with st.container(border=True):
            st.title('Meine Quick-Daten')
            jzaehlen(st.session_state['loggedinuserid'])
    else:
        st.switch_page('main.py')