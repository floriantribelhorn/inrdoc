import streamlit as st
#beim Ausloggen alle session_state variablen zurücksetzen (leeren)
for key in st.session_state.keys():
    del st.session_state[key]
st.switch_page('main.py')