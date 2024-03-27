import streamlit as st
from functions.functions1_new import *
from functions.database_new import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if __name__ == '__main__':
    main(st.session_state['loginstatus'])
    jahre = list()
    for i in range(100):
        if i < 10:
            jahre.append('190'+str(i))
        else:
            jahre.append('19'+str(i))
    for e in range(25):
        if e < 10:
            jahre.append('200'+str(e))
        else:
            jahre.append('20'+str(e))
    jahre.reverse()
    with st.container(border=True):
        bereich = st.selectbox('Wählen Sie das gewünschte Jahr aus',(jahre))
    editoranzeige(st.session_state['loggedinuserid'],bereich)
