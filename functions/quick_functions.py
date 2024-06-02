#benötigte Skripts/Libraries importieren
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mysql.connector
import plotly.graph_objects as go
import time
from functions.cnx import *
import math
from datetime import datetime

#Funktion zum Ausgeben der gespeicherten Daten in Form von einer mit plotly generierter Grafik
def quick_data_check(user, dauer):
    conn = mysql.connector.connect(**connex())
    #Alle Daten von "user" aus mainDB auslesen und nach Datum ordnen (absteigend = neustes zuerst)
    sql_query = f"""
    SELECT * FROM `sql7710143`.`main_quick_data` WHERE user = {user} ORDER BY `datum` ASC
    """
    #mit pandas dataframe zurechtrücken (zwei Spalten droppen), sortieren (datum, inr) und mit df.head auf ausgewählte Dauer stutzen
    df = pd.read_sql(sql_query, conn)
    df = df.drop(columns=['id','user'])
    df = df.sort_values('datum') 
    df['inr'] = df['inr'].astype(float)  
    df = df.sort_values(by=['datum', 'inr'],ascending=False)  
    df = df.head(dauer)    

    #plotly graph Objekte aus dataframe definieren sowie aus Datenbank Namen des users und INR-Zielwerte abrufen
    fig = go.Figure(data=go.Scatter(x=df['datum'], y=df['inr'], mode='lines'))
    cursor = conn.cursor()
    cursor.execute('SELECT `vorname` FROM `sql7710143`.`user_data` WHERE id = %s', (user,))
    rows = cursor.fetchall()
    conn.close()

    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute(f'SELECT `lower`,`upper` FROM `sql7710143`.`targetlevel` WHERE `user` = %s', (user,))
    row = cursor.fetchone()
    conn.close()
    #Zielwerte in Variabeln abspeichern
    lower, upper = row

    #plotly Graphen erstellen
    fig.update_layout(
        xaxis=dict(title='Datum', tickformat='%Y-%m-%d'),
        yaxis=dict(title='INR'),
        title=f'Quick Daten (INR-Zielbereich) von {rows[0][0]} letzte {dauer} Dateneinträge',
        shapes=[
        #Referenzlinie "lower"
        dict(
            type='line',
            x0=df['datum'].min(),
            y0=lower,
            x1=df['datum'].max(),
            y1=lower,
            line=dict(
                color='red',
                width=2,
                dash='dash'
            )
        ),
        #Referenzlinie "upper"
        dict(
            type='line',
            x0=df['datum'].min(),
            y0=upper,
            x1=df['datum'].max(),
            y1=upper,
            line=dict(
                color='red',
                width=2,
                dash='dash'
            )
        )
        ]
    )
    st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")
    conn.close()

#Funktion zur Überprüfung, ob am gewählten Datum bereits ein Quick gespeichert wurde
def quick_empty(user, date):
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute(f'SELECT `datum` FROM `sql7710143`.`main_quick_data` WHERE datum = %s AND user = %s', (date,user,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        return True
    else:
        return False

#Funktion zum Abspeichern eines eingetragenen INR-Werts
def quick_eintrag(quick,inr,date):
    #vorerst abrufen, welches Medikament der user verwendet und welches sein aktuelles LOT-Nr. ist
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    id = st.session_state['loggedinuserid']
    cursor.execute(f'SELECT `med` FROM `sql7710143`.`user_data` WHERE id = %s', (id,))
    rows = cursor.fetchone()
    conn.close()
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    id = st.session_state['loggedinuserid']
    cursor.execute(f'SELECT `lot_data`.`new_lot`, `lot_data`.`id` FROM `sql7710143`.`lot_data` JOIN `lot_numbers` ON `lot_data`.`new_lot` = `lot_numbers`.`id` WHERE `user` = %s ORDER BY `lot_data`.`id` DESC LIMIT 1', (id,))
    rows2 = cursor.fetchone()
    current_lot = rows2[0]
    conn.close()
    #nur weiter, wenn auch schon Medikament erfasst ist
    if rows != 0:
        med2 = rows[0]
        conn = mysql.connector.connect(**connex())
        cursor = conn.cursor()
        #die verschiedenen Daten in Tabelle eintragen -> quick, inr und date kommen von der Editor-Seite, id,med2 und current lot wurden in der Funktion definiert
        cursor.execute(f"""
            INSERT INTO `sql7710143`.`main_quick_data` (quick, inr, datum, user, medi, lot_nr)
            VALUES (%s,%s,%s,%s,%s, %s)
            """, (quick,inr,date,id,med2,current_lot))
        conn.commit()
        conn.close()
        #solange Daten an DB geschickt werden kurzer Progress-Balken
        progress_text = "Quick wird gespeichert, bitte warten bis Meldung in grün erscheint!"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        my_bar.empty()
        #nochmals DB-connection zum erfolgreichen Speichern überprüfen und st.success mit ausgelesenen neuen Daten
        conn = mysql.connector.connect(**connex())
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT `quick` from `sql7710143`.`main_quick_data` WHERE datum = %s AND user = %s""", (date,id))
        rows = cursor.fetchall()
        if rows:
            date1 = date.strftime('%d-%m-%Y')
            st.success(f'Quick vom {date1} wurde gespeichert!')
        conn.commit()
        conn.close()
    else:
        st.info('Sie haben noch kein Medikament in Ihrem Profil erfasst!')

#Funktion zum Anpassen der INR-Zielwerte im Profil-Bereich (sign_up.py)
def inr_bereich(userid):
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT `lower`,`upper` FROM `sql7710143`.`targetlevel` WHERE user = %s""", (userid,))
    row = cursor.fetchone()
    lower, upper = row
    conn.close()
    with st.expander(label='Mein INR-Zielbereich',expanded=False):
        st.subheader('Mein INR-Zielbereich')
        unter = st.number_input(label='Untere INR-Grenze',value=lower,min_value=0.0,max_value=10.0,step=0.1)
        ober = st.number_input(label='Obere INR-Grenze',value=upper,min_value=0.0,max_value=10.0,step=0.1)
        btn = st.button(label='Zielbereiche anpassen')
        if btn:
            if ober > unter:
                conn = mysql.connector.connect(**connex())
                cursor = conn.cursor()
                cursor.execute(f'''UPDATE `sql7710143`.`targetlevel` SET `lower`= %s,`upper`= %s WHERE `user` = %s''', (unter,ober,userid))
                num_rows_updated = cursor.rowcount
                conn.commit()
                conn.close()
                if num_rows_updated:
                    st.success('Zielwert angepasst',icon='🚨')
                else:
                    st.warning('Etwas ist schiefgelaufen!',icon='"🔥')
            elif upper == lower:
                st.info('INR-Zielbereiche sind identisch, keine Aktualisierung erfolgt!')
            else:
                st.info('Unterer INR-Zielwert ist grösser als der obere, keine Aktualisierung erfolgt!')

#Funktion zum Löschen von ausgewählten Einträgen bei editor.py, resp. diese Funktion wird in folgender Fkt (quick_daten()) gebraucht
def loeschen_eintraege(daten,user):
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    cursor.execute(f"""
        DELETE FROM `sql7710143`.`main_quick_data` WHERE datum = %s AND user = %s""", (daten,user,))
    num_rows_deleted = cursor.rowcount
    if num_rows_deleted == 1:
        st.success(f"Eintrag vom {daten} wurde erfolgreich gelöscht.")
    elif num_rows_deleted > 1:
        st.success(f"{num_rows_deleted} Einträge {daten} wurde erfolgreich gelöscht.")
    else:
        st.warning(f"Kein Eintrag mit :blue[Datum] {daten} wurde gefunden.")
    conn.commit()
    conn.close()

#Funktion zum Auslesen aller bisher erfassten Daten eines users + Ordnung nach Jahr und Monaten incl. Lösch-Fkt (siehe vorgehende Fkt)
def quick_daten(user):
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    #sql-query zum Zählen von Daten-Einträgen sortiert nach Jahr und Monat (beides aufsteigend)
    sqlquery = f"""
    SELECT YEAR(`datum`) AS Year, MONTH(`datum`) AS Month, COUNT(*) AS Count
    FROM `main_quick_data`
    WHERE user = {user}
    GROUP BY Year, Month
    ORDER BY Year ASC, Month ASC;
    """
    cursor.execute(sqlquery)
    rows = cursor.fetchall()

    if rows:
        #obige Daten in dataframe speichern
        df = pd.read_sql(sqlquery, conn)

        #Jahr-Tabs erstellen für jedes Jahr mit Daten
        tab_titles = [f'Jahr {year}' for year in df['Year'].unique()]
        tabs = st.tabs(tab_titles)

        #jedes Jahr-Tab iterieren
        for i, year in enumerate(df['Year'].unique()):
            with tabs[i]:
                #Subtabs für jeden Monat im dazupassenden Jahr-Tab erstellen
                subtab_titles = [f'Monat {month}' for month in df[df['Year'] == year]['Month'].unique()]
                subtabs = st.tabs(subtab_titles)

                #jedes Monat-Tab iterieren, um die dazupassenden Quick-Daten als Checkbox auszugeben
                for j, month in enumerate(df[df['Year'] == year]['Month'].unique()):
                    with subtabs[j]:
                        conn = mysql.connector.connect(**connex())
                        #aus HauptDB passende Jahr/Monat Quick-Daten abrufen
                        sql_query = f"""
                        SELECT * FROM `main_quick_data` 
                        WHERE YEAR(datum) = {year} AND MONTH(datum) = {month} AND user = {user} 
                        ORDER BY `datum` ASC
                        """
                        df_month = pd.read_sql(sql_query, conn)
                        df_month = df_month.drop(columns=['id','user'])
                        df_month = df_month.sort_values('datum') 
                        df_month['quick'] = df_month['quick'].astype(float)  
                        df_month = df_month.sort_values(by=['datum', 'quick'],ascending=False) 
                        df_month['checkbox'] = df_month.index
                        conn.close()

                        num_checks = len(df_month)
                        num_cols = (num_checks // 25) + (num_checks % 25 > 0)
                        cols = st.columns(num_cols)

                        with st.form(key=f'loeschen{i}_{j}'):
                            checked_boxes = {}
                            for k, row in df_month.iterrows():
                                with cols[k % num_cols]:
                                    int_part = math.floor(row['quick'])
                                    num_dig = len(str(int_part))
                                    gerundeterquick = round(row['quick'],num_dig) 
                                    checked_boxes[row['datum']] = st.checkbox(label=f":blue[Datum]: {row['datum']} - :orange[Quick]: {gerundeterquick}", key=f'value_from_{row["datum"]}')
                                    if f'value_from_{row["datum"]}' not in st.session_state:
                                        st.session_state[f'value_from_{row["datum"]}'] = False
                            submit_button = st.form_submit_button(label='Einträge :red[LÖSCHEN]')
                            if submit_button:
                                selected_dates = [date for date, checked in checked_boxes.items() if checked]
                                for row in selected_dates:
                                    loeschen_eintraege(row,st.session_state['loggedinuserid'])
                                else:
                                    st.rerun()
    else:
        st.info('Sie haben noch keine Messdaten erfasst.')   