import streamlit as st
import numpy as np
from functions.database_new import *
from functions.functions1_new import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if 'loggedinuser' not in st.session_state:
    st.session_state['loggedinuser'] = False

if 'loggedinuserid' not in st.session_state:
    st.session_state['loggedinuserid'] = False

if 'aktuell' not in st.session_state:
    st.session_state['aktuell'] = 'Hauptseite'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])
    user_database()
    setup_quickdatabase(st.session_state['loggedinuserid'])
