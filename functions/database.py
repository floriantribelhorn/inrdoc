import sqlite3
import os
import streamlit as st

def user_database():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS user_data (id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            vorname TEXT NOT NULL,
            nachname TEXT NOT NULL,
            register_date TEXT NOT NULL,
            birthdate TEXT NOT NULL,
            password TEXT NOT NULL)
                   """)

    conn.commit()
    conn.close()

def setup_quickdatabase(someoneloggedin):
    if someoneloggedin != False:
        conn = sqlite3.connect("quick_data.db")
        cursor = conn.cursor()
        currentuser = st.session_state['loggedinuser']
        tablename = f'quick_data_from_{currentuser}'
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tablename} (id INTEGER PRIMARY KEY AUTOINCREMENT,
                quick TEXT NOT NULL,
                datum TEXT NOT NULL,
                user TEXT NOT NULL)
                    """)

        conn.commit()
        conn.close()