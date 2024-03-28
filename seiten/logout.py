import streamlit as st
import numpy as np
from functions.database_new import *
from functions.functions1_new import *

st.session_state['loginstatus'] = False
st.session_state['loggedinuser'] = False
st.switch_page('main.py')