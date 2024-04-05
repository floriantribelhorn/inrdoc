import streamlit as st
from functions.database_new import *
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if 'loggedinuser' not in st.session_state:
    st.session_state['loggedinuser'] = False

if 'loggedinuserid' not in st.session_state:
    st.session_state['loggedinuserid'] = False

if 'aktuell' not in st.session_state:
    st.session_state['aktuell'] = 'Startseite'
else:
    st.session_state['aktuell'] = 'Startseite'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])
    user_database()
    setup_quickdatabase(st.session_state['loggedinuserid'])