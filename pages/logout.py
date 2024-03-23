import streamlit as st
import numpy as np
from functions.database import *
from functions.functions1 import *

st.session_state['loginstatus'] = False
st.session_state['loggedinuser'] = False
st.switch_page('main.py')