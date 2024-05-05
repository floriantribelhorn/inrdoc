import streamlit as st
import mysql.connector
from functions.cnx import *

def user_database():
    conn = mysql.connector.connect(**connex())
    cur = conn.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS`freedb_inrdoc`.`user_data` (`id` INT NOT NULL AUTO_INCREMENT , `username` TEXT NOT NULL ,
             `vorname` TEXT NOT NULL , `nachname` TEXT NOT NULL , `register_date` DATE NOT NULL ,
             `birthdate` DATE NOT NULL , `password` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;""")
    conn.commit()
    conn.close()

def setup_quickdatabase(someoneloggedin):
    conn = mysql.connector.connect(**connex())
    cur = conn.cursor()
    if someoneloggedin != False:
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS `freedb_inrdoc`.`main_quick_data` (`id` INT NOT NULL AUTO_INCREMENT, 
                    `quick` TEXT NOT NULL,
                    `datum` DATE NOT NULL,
                    `user` TEXT NOT NULL,
                    `medi` INT NOT NULL,
                    PRIMARY KEY (`id`)) ENGINE = InnoDB;""")
    conn.commit()
    conn.close()