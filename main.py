import streamlit as st
import numpy as np
from functions.database import *
from functions.functions1 import *
#import st_pages as stp

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if 'loggedinuser' not in st.session_state:
    st.session_state['loggedinuser'] = False

if __name__ == '__main__':
    main(st.session_state['loginstatus'])
    user_database()
    setup_quickdatabase(st.session_state['loggedinuser'])