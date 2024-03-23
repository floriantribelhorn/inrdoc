import streamlit as st
from functions.functions1 import *
from functions.database import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if __name__ == '__main__':
    main(st.session_state['loginstatus'])
    editoranzeige(st.session_state['loggedinuser'])