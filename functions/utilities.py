import streamlit as st
import hashlib

def main(logstate):
    st.set_page_config(page_title='INR Dokumentation', page_icon="🏠", layout="wide", initial_sidebar_state="expanded")
    if logstate != True:
        st.subheader("Zur Zeit ist niemand eingeloggt, bitte loggen Sie sich links in der Navigation ein!")
    #st.subheader(f"Hallo {st.session_state['loggedinuser']}! {st.session_state['aktuell']}")
    if logstate == True:
        st.sidebar.title("Navigation")
        st.sidebar.page_link("main.py", label="Startseite", icon = "🏠")
        st.sidebar.page_link("pages/sign_up.py", label="Login/Registration", icon = "🔒")
        st.sidebar.page_link("pages/overview.py", label="Überblick", icon = "🩺")
        st.sidebar.page_link("pages/messeingabe.py", label="Messungen", icon = "🩸")
        st.sidebar.page_link("pages/editor.py", label="Editor", icon = "🧮")
        st.sidebar.page_link("pages/logout.py", label = "Ausloggen", icon = "⏹️")
    else:
        st.sidebar.page_link("pages/sign_up.py", label="Login", icon = "🔒")

def md5sum(t):
    return hashlib.md5(t.encode('utf-8')).hexdigest()

def empty_check(a,b,c,d,e,f):
    if a != '' and b != '' and c != '' and d != '' and e != '' and f != '':
        return True
    else:
        return False 

def empty_check2(a,b):
    if a != '' and b != '':
        return True
    else:
        return False
    
def proceed_login():
    st.session_state['einloggen'] = True
    st.session_state['registrieren'] = False
    st.rerun()

def proceed_register():
    st.session_state['registrieren'] = True
    st.session_state['einloggen'] = False
    st.rerun()

def zeitraum(zeitraum):
    if zeitraum == '5 Tage':
        zeitraum2 = 5
    elif zeitraum == '10 Tage':
        zeitraum2 = 10
    elif zeitraum == '30 Tage':
        zeitraum2 = 30
    elif zeitraum == '2 Monate':
        zeitraum2 = 60
    elif zeitraum == '6 Monate':
        zeitraum2 = 180
    elif zeitraum == '1 Jahr':
        zeitraum2 = 360
    return zeitraum2