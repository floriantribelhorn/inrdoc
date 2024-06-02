#benötigte Skripts/Libraries importieren
import streamlit as st
from functions.cnx import *
import mysql.connector
import hashlib
from datetime import datetime as dt
from datetime import timedelta as td

#Navigations-Funktion, set_page_config + je nach Login-Status Anzeige "normales Menü für registrierte User" oder "Menü für noch nicht registrierte"
def main(log):
    st.set_page_config(page_title='INR Dokumentation', page_icon="🏠", layout="wide", initial_sidebar_state="expanded")
    
    if log == True:
        st.sidebar.title("Navigation")
        st.sidebar.page_link("main.py", label="Startseite", icon = "🏠")
        st.sidebar.page_link("pages/sign_up.py", label="Login/Registration", icon = "🔒")
        st.sidebar.page_link("pages/overview.py", label="Überblick", icon = "🩺")
        st.sidebar.page_link("pages/messeingabe.py", label="Messungen", icon = "🩸")
        st.sidebar.page_link("pages/editor.py", label="Editor", icon = "🧮")
        st.sidebar.page_link("pages/logout.py", label = "Ausloggen", icon = "⏹️")
        st.sidebar.text(f"Hallo {st.session_state['loggedinuser']}!")
    else:
        st.sidebar.page_link("pages/sign_up.py", label="Login", icon = "🔒")
        st.sidebar.text('Loggen Sie sich ein!')

#Funktion: Passwort unkenntlich machen (bei Registrierung und Login)
def md5sum(t):
    return hashlib.md5(t.encode('utf-8')).hexdigest()

#Funktion, ob 6 Text-Inputs leer sind
def empty_check(a,b,c,d,e,f):
    if a != '' and b != '' and c != '' and d != '' and e != '' and f != '':
        return True
    else:
        return False 
    
#Funktion, ob 2 Text-Inputs leer sind
def empty_check2(a,b):
    if a != '' and b != '':
        return True
    else:
        return False
    
#Funktion, ob 7 Text-Inputs leer sind
def empty_check3(a,b,c,d,e,f,g):
    if a != '' and b != '' and c != '' and d != '' and e != '' and f != '' and g != '':
        return True
    else:
        return False 
    
#Funktion, ob ein Datum in der Vergangenheit liegt (Reagenz/LOT abgelaufen?)
def is_expired(expiry: str) -> bool:
    expiry_date = dt.strptime(expiry, '%Y-%m-%d')
    today = dt.today()
    return expiry_date < today

#Funktionen die Session-States so ändert, dass andere Buttons/Forms angezeigt werden beim Login/Registrierung
def proceed_login():
    st.session_state['einloggen'] = True
    st.session_state['registrieren'] = False
    st.rerun()

def proceed_register():
    st.session_state['registrieren'] = True
    st.session_state['einloggen'] = False
    st.rerun()

#Funktion zur Umwandlung von Anzahl Tagen in Textform zu Anzahl Tagen in integer Form
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

#Funktion zum Überprüfen, ob ein Datum in der Zukunft liegt
def futuredate(date):
    today = dt.today().date()
    if date > today + td(0):
        return True
    else:
        return False

#je einmal Abruf, welche Medikamente, Geräte zur Auswahl stehen und in 2 dicts abspeichern    
conn = mysql.connector.connect(**connex())
cursor = conn.cursor()
cursor.execute('SELECT `drug_name`,`drug_nr` FROM `sql7710143`.`drugs`')
rows = cursor.fetchall()
drugs_dict = {}
for name, nr in rows:
    drugs_dict[name] = nr
conn.close()

conn = mysql.connector.connect(**connex())
cursor = conn.cursor()
cursor.execute('SELECT `device_name`,`device_nr` FROM `sql7710143`.`devices`')
rows = cursor.fetchall()
device_dict = {}
for name, nr in rows:
    device_dict[name] = nr
conn.close()

#Funktion zum Überprüfen, welches Gerät vom jeweiligen User verwendet wird
def mydevice(user):
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('SELECT `new_device` FROM `sql7710143`.`device_data` WHERE `user` = %s ORDER BY `updated` DESC LIMIT 1',(user,))
    rows = cursor.fetchone()
    conn.close()
    return rows[0]