import streamlit as st
import mysql.connector

cnxn_str = {
    'user': st.secrets.db_credentials.user,
    'password': st.secrets.db_credentials.password,
    'host': st.secrets.db_credentials.host,
    'database': st.secrets.db_credentials.database,
    'port': st.secrets.db_credentials.port,
    'auth_plugin': st.secrets.db_credentials.auth_plugin
}

def user_database():
    
    conn = mysql.connector.connect(**cnxn_str)
    cur = conn.cursor()

    cur.execute(""" CREATE TABLE IF NOT EXISTS`freedb_inrdoc`.`user_data` (`id` INT NOT NULL AUTO_INCREMENT , `username` TEXT NOT NULL ,
             `vorname` TEXT NOT NULL , `nachname` TEXT NOT NULL , `register_date` DATE NOT NULL ,
             `birthdate` DATE NOT NULL , `password` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;""")

    conn.commit()
    conn.close()

def setup_quickdatabase(someoneloggedin):

    conn = mysql.connector.connect(**cnxn_str)
    cur = conn.cursor()
    
    if someoneloggedin != False:
        cur = conn.cursor()
        currentuserid = st.session_state['loggedinuserid']
        tablename = f'quick_data_from_{currentuserid}'
        cur.execute(f"""CREATE TABLE IF NOT EXISTS `freedb_inrdoc`.`{tablename}` (`id` INT NOT NULL AUTO_INCREMENT, 
                    `quick` TEXT NOT NULL,
                    `datum` DATE NOT NULL,
                    `user` TEXT NOT NULL,
                    PRIMARY KEY (`id`)) ENGINE = InnoDB;""")

        conn.commit()
        conn.close()
