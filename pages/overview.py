#benötigte Skripts/Libraries importieren
import streamlit as st
from functions.utilities import *
from functions.quick_functions import *
from functions.cnx import *

#session_state Variable initialisieren falls overview.py direkt aufgerufen wird
if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

st.session_state['aktuell'] = 'Datenüberblick'

#Navigation anzeigen
if __name__ == '__main__':
    main(st.session_state['loginstatus'])

#falls eingeloggt, Möglichkeit Zeitraum auswählen und die letzten X Daten als Grafik ausgeben
if st.session_state['loginstatus'] != False:
    with st.expander(label='Zeitraum anzeigen',expanded=False):
        zeit = st.selectbox('Quick-Werte Zeitraum:', ('5 Tage','10 Tage', '30 Tage', '2 Monate','6 Monate','1 Jahr'))
        zeigen = st.button('Werte ausgeben')

    if zeigen:
        dauer = zeitraum(zeit)
        quick_data_check(st.session_state['loggedinuserid'],dauer)
else:
#falls nicht eingeloggt -> umleiten auf Hauptseite
    st.switch_page('main.py')
