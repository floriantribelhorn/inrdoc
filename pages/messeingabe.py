import streamlit as st
from functions.functions1_new import *
from functions.database_new import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if __name__ == '__main__':
    main(st.session_state['loginstatus'])

with st.container(border=True):
    st.subheader('Quick-Eingabe')
    heutigerquick = st.number_input(label = "Quick-Messwert", min_value=0, max_value=100, step=1)
    datum = st.date_input('Zeitpunkt der Messung')
    abspeichern = st.button('Quick jetzt abspeichern')
    if abspeichern:
        if not quick_empty(st.session_state['loggedinuser'],datum):
            quick_eintrag(heutigerquick,datum)
        else:
            st.write('An diesem Datum existiert bereits eine eingetragene Messung')