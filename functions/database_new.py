import streamlit as st
import mysql.connector

cnxn_str = {
    'user': 'freedb_inrdocuser',
    'password': '?$R8*?pKxKvmg5X',
    'host': 'sql.freedb.tech',
    'database': 'freedb_inrdoc',
    'port': '3306',
    'auth_plugin':'mysql_native_password'
}

def user_database():
    
    conn = mysql.connector.connect(**cnxn_str)
    cur = conn.cursor()

    cur.execute(""" CREATE TABLE IF NOT EXISTS`freedb_inrdoc`.`user_data` (`id` INT NOT NULL AUTO_INCREMENT , `username` TEXT NOT NULL ,
             `vorname` TEXT NOT NULL , `nachname` TEXT NOT NULL , `register_date` TEXT NOT NULL ,
             `birthdate` TEXT NOT NULL , `password` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;""")

    conn.commit()
    conn.close()

def setup_quickdatabase(someoneloggedin):

    conn = mysql.connector.connect(**cnxn_str)
    cur = conn.cursor()
    
    if someoneloggedin != False:
        cur = conn.cursor()
        currentuser = st.session_state['loggedinuser']
        tablename = f'quick_data_from_{currentuser}'
        cur.execute(f"""CREATE TABLE IF NOT EXISTS `freedb_inrdoc`.`{tablename}` (`id` INT NOT NULL AUTO_INCREMENT, 
                    `quick` TEXT NOT NULL,
                    `datum` TEXT NOT NULL,
                    `user` TEXT NOT NULL,
                    PRIMARY KEY (`id`)) ENGINE = InnoDB;""")

        conn.commit()
        conn.close()