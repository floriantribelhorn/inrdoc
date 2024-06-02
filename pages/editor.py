#benötigte Skripts/Libraries importieren
import streamlit as st
from functions.utilities import *
from functions.quick_functions import *
from functions.cnx import *

#session_state Variablen initialisieren
if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

st.session_state['aktuell'] = 'Dateneditor'

#Navigation + falls eingeloggt alle erfassten Quick-Daten anzeigen
if __name__ == '__main__':
    main(st.session_state['loginstatus'])
    if st.session_state['loginstatus'] != False:
        with st.container(border=True):
            st.title('Meine Quick-Daten')
            quick_daten(st.session_state['loggedinuserid'])
    else:
        #wenn nicht eingeloggt zurück zur Startseite
        st.switch_page('main.py')