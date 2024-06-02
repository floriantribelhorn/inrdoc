import streamlit as st
import mysql.connector
from functions.cnx import *

#user DB anlegen, falls nicht schon passiert
def user_database():
    conn = mysql.connector.connect(**connex())
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS `sql7710143`.`user_data` (`id` INT NOT NULL AUTO_INCREMENT , `username` TEXT NOT NULL ,
             `vorname` TEXT NOT NULL , `nachname` TEXT NOT NULL , `register_date` DATE NOT NULL ,
             `birthdate` DATE NOT NULL , `password` TEXT NOT NULL, `med` INT NOT NULL, PRIMARY KEY (`id`)) ENGINE = InnoDB;""")
    conn.commit()
    conn.close()

#main_quick_data (zentrale INR/Quick-DB) anlegen, falls nicht schon passiert
def setup_quickdatabase(someoneloggedin):
    conn = mysql.connector.connect(**connex())
    cur = conn.cursor()
    if someoneloggedin != False:
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS `sql7710143`.`main_quick_data` (`id` INT NOT NULL AUTO_INCREMENT, 
                    `quick` FLOAT NOT NULL,
                    `inr` FLOAT NOT NULL,
                    `datum` DATE NOT NULL,
                    `user` INT NOT NULL,
                    `medi` INT NOT NULL,
                    `lot_nr` INT NOT NULL,
                    PRIMARY KEY (`id`)) ENGINE = InnoDB;""")
    conn.commit()
    conn.close()

#Zielwerte (INR) DB anlegen, falls nicht schon passiert
def setup_targetlevel(someoneloggedin):
    conn = mysql.connector.connect(**connex())
    cur = conn.cursor()
    if someoneloggedin != False:
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS `sql7710143`.`targetlevel` (`id` INT NOT NULL AUTO_INCREMENT, 
                    `upper` FLOAT NOT NULL,
                    `lower` FLOAT NOT NULL,
                    `user` INT NOT NULL,
                    PRIMARY KEY (`id`)) ENGINE = InnoDB;""")
    conn.commit()
    conn.close()

#Lot-Nr. DB anlegen, falls nicht schon passiert
def setup_lotnrdb(someoneloggedin):
    conn = mysql.connector.connect(**connex())
    cur = conn.cursor()
    if someoneloggedin != False:
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS `sql7710143`.`lot_numbers` (`id` INT NOT NULL AUTO_INCREMENT, 
                    `lotnr` TEXT NOT NULL,
                    `device` INT NOT NULL,
                    `expiry` DATE NOT NULL,
                    `isi` FLOAT NOT NULL,
                    `refquick` INT NOT NULL,
                    PRIMARY KEY (`id`)) ENGINE = InnoDB;""")
    conn.commit()
    conn.close()

#Lot-Nr. Rückverfolgbarkeits DB anlegen, falls nicht schon passiert
def setup_lotnrdb2(someoneloggedin):
    conn = mysql.connector.connect(**connex())
    cur = conn.cursor()
    if someoneloggedin != False:
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS `sql7710143`.`lot_data` (`id` INT NOT NULL AUTO_INCREMENT, 
                    `old_lot` INT,
                    `new_lot` INT NOT NULL,
                    `updated` DATETIME NOT NULL,
                    `user` INT NOT NULL,
                    PRIMARY KEY (`id`)) ENGINE = InnoDB;""")
    conn.commit()
    conn.close()

#Medikamenten DB anlegen, falls nicht schon passiert
def setup_meddb(someoneloggedin):
    conn = mysql.connector.connect(**connex())
    cur = conn.cursor()
    if someoneloggedin != False:
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS `sql7710143`.`drugs` (`drug_nr` INT NOT NULL AUTO_INCREMENT, 
                    `drug_name` TEXT NOT NULL,
                    PRIMARY KEY (`drug_nr`)) ENGINE = InnoDB;""")
    conn.commit()
    conn.close()

#Geräte Rückverfolgbarkeit DB anlegen, falls nicht schon passiert
def setup_devicedb(someoneloggedin):
    conn = mysql.connector.connect(**connex())
    cur = conn.cursor()
    if someoneloggedin != False:
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS `sql7710143`.`device_data` (`idn` INT NOT NULL AUTO_INCREMENT, 
                    `old_device` INT,
                    `new_device` INT NOT NULL,
                    `updated` DATETIME NOT NULL,
                    `user` INT NOT NULL,
                    PRIMARY KEY (`idn`)) ENGINE = InnoDB;""")
    conn.commit()
    conn.close()

#Geräte DB anlegen, falls nicht schon passiert
def setup_devicedb2(someoneloggedin):
    conn = mysql.connector.connect(**connex())
    cur = conn.cursor()
    if someoneloggedin != False:
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS `sql7710143`.`devices` (`device_nr` INT NOT NULL AUTO_INCREMENT, 
                    `device_name` TEXT NOT NULL,
                    PRIMARY KEY (`device_nr`)) ENGINE = InnoDB;""")
    conn.commit()
    conn.close()