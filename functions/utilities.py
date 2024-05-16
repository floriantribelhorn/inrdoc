import streamlit as st
from functions.cnx import *
import mysql.connector
import hashlib
from datetime import datetime as dt
from datetime import timedelta as td

def main(logstate):
    st.set_page_config(page_title='INR Dokumentation', page_icon="🏠", layout="wide", initial_sidebar_state="expanded")
    
    if logstate == True:
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

def empty_check3(a,b,c,d,e,f,g):
    if a != '' and b != '' and c != '' and d != '' and e != '' and f != '' and g != '':
        return True
    else:
        return False 
    
def is_expired(expiry: str) -> bool:
    expiry_date = dt.strptime(expiry, '%Y-%m-%d')
    today = dt.today()
    return expiry_date < today
    
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

def quick_formula_calc_inr(quick,isi,refquick):
    inr = (quick/refquick)**isi
    return inr

def quick_formula_calc_inr2(quick,isi):
    inr = (quick/30)**isi
    return inr

def quick_formula_calc_quick(inr,isi,refquick):
    quick = (inr**(1/isi))*refquick
    return quick

def futuredate(date):
    today = dt.today().date()
    if date > today + td(0):
        return True
    else:
        return False
    
conn = mysql.connector.connect(**connex())
cursor = conn.cursor()
cursor.execute('SELECT `drug_name`,`drug_nr` FROM `freedb_inrdoc`.`drugs`')
rows = cursor.fetchall()
drugs_dict = {}
for name, nr in rows:
    drugs_dict[name] = nr
conn.close()

conn = mysql.connector.connect(**connex())
cursor = conn.cursor()
cursor.execute('SELECT `device_name`,`device_nr` FROM `freedb_inrdoc`.`devices`')
rows = cursor.fetchall()
device_dict = {}
for name, nr in rows:
    device_dict[name] = nr
conn.close()

def mydevice(user):
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute('SELECT `new_device` FROM `freedb_inrdoc`.`device_data` WHERE `user` = %s ORDER BY `updated` DESC LIMIT 1',(user,))
    rows = cursor.fetchone()
    return rows[0]
    conn.close()