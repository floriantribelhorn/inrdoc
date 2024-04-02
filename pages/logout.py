import streamlit as st
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *

for key in st.session_state.keys():
    del st.session_state[key]
st.switch_page('main.py')