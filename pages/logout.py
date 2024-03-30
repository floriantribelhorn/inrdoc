import streamlit as st
import numpy as np
from functions.database_new import *
from functions.functions1_new import *

for key in st.session_state.keys():
    del st.session_state[key]
st.switch_page('main.py')