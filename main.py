import streamlit as st
from functions.database_new import *
from functions.utilities import *
from functions.user_functions import *
from functions.quick_functions import *
from functions.cnx import *

if 'loginstatus' not in st.session_state:
    st.session_state['loginstatus'] = False

if 'loggedinuser' not in st.session_state:
    st.session_state['loggedinuser'] = False

if 'loggedinuserid' not in st.session_state:
    st.session_state['loggedinuserid'] = False

if 'medikament' not in st.session_state:
    st.session_state['medikament'] = False

if 'aktuell' not in st.session_state:
    st.session_state['aktuell'] = 'Startseite'
else:
    st.session_state['aktuell'] = 'Startseite'

if __name__ == '__main__':
    main(st.session_state['loginstatus'])
    user_database()
    setup_quickdatabase(st.session_state['loggedinuserid'])
    with st.container(border=True):
        st.title('International Normalized Ratio')
        st.header('1. Definition')
        st.markdown('Die International Normalized Ratio, kurz INR, ist ein weltweit in Laboratorien standardisiertes Verfahren zur Prüfung des extrinsischen Systems der Blutgerinnung. Die INR ist ein standardisierter Quick-Wert und löst diesen ab. Der Quick-Wert ist methodenabhängig und liefert mit unterschiedlichen Testkits unterschiedliche, untereinander nicht vergleichbare Befunde.')
        st.header('2. Hintergrund')
        st.markdown('Der Quick-Wert variiert je nach Empfindlichkeit des Thromboplastins. Diese ist u.a. davon abhängig, aus welchem Organismus (z.B. Kaninchen, Rind oder Mensch) und welchem Organ (Lunge, Gehirn oder Plazenta) das Thromboplastin gewonnen wurde. Um Variabilität für die Berechnung der INR auszugleichen, wird der International Sensitivity Index (ISI) eingesetzt. Dieser Index wird im Vergleich zu einem Referenz-Thromboplastin bestimmt, das bereits 1983 durch die WHO definiert wurde.')
        st.header('3. Berechnung')
        st.latex(r'''\frac{Gerinnungszeit Patientenplasma}{Gerinnungszeit Normalplasma}''')
        st.header('4. Interpretation')
        st.markdown('Die INR verhält sich zum Quick-Wert umgekehrt proportional: -Mit abnehmendem Quick-Wert wird die INR größer -Mit zunehmendem Quick-Wert wird die INR kleiner Normwertig ist eine INR von 0,85 bis 1,15. Eine INR von 1,0 entspricht dabei einem Quick-Wert von 100%. Therapeutische INR-Werte bei medikamentöser Antikoagulation liegen in der Regel zwischen 2,0 und 3,5.')
        st.header('5. Verwendung')
        st.markdown('Die INR wird hauptsächlich zur Steuerung und Verlaufskontrolle einer Antikoagulation mit Vitamin-K-Antagonisten (Phenprocoumon, Warfarin) eingesetzt. Die INR wird hierbei in der Einstellungsphase täglich, nach erfolgter Einstellung - abhängig von Patienteneigenschaften wie Compliance und Stabilität der Antikoagulation - einmal wöchentlich bis einmal monatlich kontrolliert. Die Überprüfung einer INR kann mithilfe von Systemen wie Coagu Check® durch den Patienten selbst erfolgen, ähnlich einer Blutzuckermessung.')
        st.image('docs/Screenshot 2024-04-25 205644.png', caption='Tabelle')
        st.header('6. Bewertung')
        st.markdown('Der INR wird vor allem im "steady state" einer Antikoagulation mit Vitamin-K-Antagonisten verwendet, da beim Monitoring dieser Patienten Probleme mit der Vergleichbarkeit der Quick-Werte auftraten. Teilweise geben Labore eine INR deshalb nur an, wenn der Quick-Wert vermindert ist. Diese ursprüngliche Definition wird aber immer weniger beachtet. Es ist kein Fehler, z.B. bei Patienten mit Leberversagen weiterhin einen Quick-Wert anzugeben. Bei der aktivierten partiellen Thromboplastinzeit (aPTT) sind die Ergebnisse zwischen unterschiedlichen Laboren ebenfalls nicht ohne Weiteres vergleichbar, hier waren die Standardisierungsbemühungen aber bisher weniger erfolgreich.')
        st.text('Quelle: DocCheck-Flexikon')
