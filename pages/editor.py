import streamlit as st
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if 'anzeigebutton' not in st.session_state:
    st.session_state['anzeigebutton'] = False

st.session_state['aktuell'] = 'Dateneditor'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])
    if st.session_state['loginstatus'] != False:
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
            if bereich:
                click = st.button(label=f'Daten aus {bereich} Anzeigen')
                if click:
                    editoranzeige(st.session_state['loggedinuserid'],bereich)