from datetime import datetime
import streamlit as st
import hashlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mysql.connector

cnxn_str = {
    'user': 'freedb_inrdocuser',
    'password': '?$R8*?pKxKvmg5X',
    'host': 'sql.freedb.tech',
    'database': 'freedb_inrdoc',
    'port': '3306',
    'auth_plugin':'mysql_native_password'
}

def md5sum(t):
    return hashlib.md5(t.encode('utf-8')).hexdigest()
                
def main(logstate):
    st.set_page_config(page_title='INR Dokumentation', page_icon="🏠", layout="wide", initial_sidebar_state="expanded")
    if logstate == True:
        st.subheader(f"Hallo {st.session_state['loggedinuser']} ! Willkommen beim Quick eintragen")
    else:
        st.subheader("Zur Zeit ist niemand eingeloggt, bitte loggen Sie sich links in der Navigation ein!")

    if logstate == True:
        st.sidebar.title("Navigation")
        st.sidebar.page_link("main.py", label="Startseite", icon = "🏠")
        st.sidebar.page_link("pages/sign_up.py", label="Login", icon = "🔒")
        st.sidebar.page_link("pages/overview.py", label="Überblick", icon = "🈺")
        st.sidebar.page_link("pages/messeingabe.py", label="Messungen", icon = "💻")
        st.sidebar.page_link("pages/editor.py", label="Editor", icon = "🈺")
        st.sidebar.page_link("pages/logout.py", label = "Ausloggen", icon = "🔒")
    else:
        st.sidebar.page_link("pages/sign_up.py", label="Login", icon = "🔒")

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
    
def username_check(username):
    if 'usernameavailable' not in st.session_state:
        st.session_state['usernameavailable'] = True
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT `username` FROM `freedb_inrdoc`.`user_data` WHERE username = %s',(username,))
    rows = cursor.fetchall()
    
    if not rows:
        st.write(f'Ein Profil mit Username: {username} wurde erstellt')
        st.session_state['usernameavailable'] = True
    else:
        st.write('Dieser Username ist schon vergeben')
        st.session_state['usernameavailable'] = False
    
    conn.commit()
    conn.close()

def user_anlegen(username,password,vorname,nachname,geburtsdatum,registerdate):
    passwordcheck = md5sum(password)
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO `freedb_inrdoc`.`user_data` (username, password, vorname, nachname, register_date, birthdate)
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (username, passwordcheck, vorname, nachname, registerdate, geburtsdatum))
    conn.commit()
    conn.close()
    

def user_einloggen(username, password):
    pw = md5sum(password)
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()

    cursor.execute('SELECT `id`,`username`, `password`,`vorname` FROM `freedb_inrdoc`.`user_data` WHERE username = %s', (username,))
    rows = cursor.fetchall()

    if len(rows) == 1:
        userid, uname, pw1, vname = rows[0]
        if uname == username and pw1 == pw:
            st.session_state['loginstatus'] = True
            st.write('logged in')
            st.session_state['loggedinuser'] = vname
            st.session_state['loggedinuserid'] = userid
            st.switch_page('main.py')
    else:
        st.write('keine Treffer')

    conn.commit()
    conn.close()

def user_data_check():
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM `freedb_inrdoc`.`user_data`')
    rows = cursor.fetchall()

    for row in rows:
        st.table(row)

    conn.commit()
    conn.close()

def quick_data_check(user, dauer):
    
    conn = mysql.connector.connect(**cnxn_str)
    tablename = f'quick_data_from_{user}'
    sql_query = f"""
    SELECT * FROM `freedb_inrdoc`.`{tablename}`
    """

    df = pd.read_sql(sql_query, conn)
    df = df.drop(columns=['id','user'])
    df = df.sort_values('datum') 
    df['quick'] = df['quick'].astype(float)  
    df = df.sort_values(by=['datum', 'quick'],ascending=False)  
    df = df.head(dauer)    

    ref_lines = [
        {'line': {'color': 'red', 'dash': 'dash'}, 'value': 55},
        {'line': {'color': 'red', 'dash': 'dash'}, 'value': 100}
    ]

    st.line_chart(df,x='datum', y='quick')

    conn.commit()
    conn.close()

def quick_empty(user, date):
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    table = f'quick_data_from_{user}'
    cursor.execute(f'SELECT `datum` FROM `freedb_inrdoc`.`{table}` WHERE datum = %s', (date,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()

    if rows:
        return True
    else:
        return False

def quick_eintrag(quick,date):
    
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    currentuser = st.session_state['loggedinuser']
    tablename = f'quick_data_from_{currentuser}'

    cursor.execute(f"""
        INSERT INTO `freedb_inrdoc`.`{tablename}` (quick, datum, user)
        VALUES (%s,%s,%s)
        """, (quick,date,st.session_state['loggedinuser']))

    conn.commit()
    conn.close()

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

def editoranzeige(user,bereich):

        conn = mysql.connector.connect(**cnxn_str)
        tablename = f'quick_data_from_{user}'
        sql_query = f"""
        SELECT * FROM `{tablename}`
        """
        
        df = pd.read_sql(sql_query, conn)
        df = df.drop(columns=['id','user'])
        df = df.sort_values('datum') 
        df['quick'] = df['quick'].astype(float)  
        df = df.sort_values(by=['datum', 'quick'],ascending=False) 
        df['checkbox'] = df.index

        conn.commit()
        conn.close()

        for i, row in df.iterrows():
            st.checkbox(label=f"{row['datum'] , row['quick']}")

def loeschen(user,werte):

    tablename = f'quick_data_from_{user}'
    
    #for i, wert in werte:
     #   cursor = conn.cursor()

      #  cursor.execute(f"""
       # DROP `{tablename}` )
