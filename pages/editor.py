import streamlit as st
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if 'anzeigebutton' not in st.session_state:
    st.session_state['anzeigebutton'] = False

st.session_state['aktuell'] = 'Dateneditor'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])
    if st.session_state['loginstatus'] != False:
        with st.container(border=True):
            jzaehlen(st.session_state['loggedinuserid'])