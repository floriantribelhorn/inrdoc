import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mysql.connector
import plotly.graph_objects as go
import time
from functions.cnx import *
from functions.utilities import *
import math

def quick_data_check(user, dauer):
    conn = mysql.connector.connect(**connex())
    sql_query = f"""
    SELECT * FROM `sql7710143`.`main_quick_data` WHERE user = {user} ORDER BY `datum` ASC
    """

    df = pd.read_sql(sql_query, conn)
    df = df.drop(columns=['id','user'])
    df = df.sort_values('datum') 
    df['inr'] = df['inr'].astype(float)  
    df = df.sort_values(by=['datum', 'inr'],ascending=False)  
    df = df.head(dauer)    

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
    
    lower, upper = row

    fig.update_layout(
        xaxis=dict(title='Datum', tickformat='%Y-%m-%d'),
        yaxis=dict(title='INR'),
        title=f'Quick Daten (INR-Zielbereich) von {rows[0][0]} letzte {dauer} Dateneinträge',
        shapes=[
        # Add the first reference line
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
        # Add the second reference line
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

def quick_eintrag(quick,inr,date):
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

    if rows != 0:
        med2 = rows[0]
        conn = mysql.connector.connect(**connex())
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO `sql7710143`.`main_quick_data` (quick, inr, datum, user, medi, lot_nr)
            VALUES (%s,%s,%s,%s,%s, %s)
            """, (quick,inr,date,id,med2,current_lot))
        conn.commit()
        conn.close()

        progress_text = "Quick wird gespeichert"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(50):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()

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

def jzaehlen(user):
    #alles = st.checkbox(label='Alles auswählen')
    conn = mysql.connector.connect(**connex())
    cursor = conn.cursor()
    sqlquery = f"""
    SELECT YEAR(`datum`) AS Year, COUNT(*) AS Count
    FROM `main_quick_data`
    WHERE user = {user}
    GROUP BY Year
    ORDER BY Year ASC;
    """
    cursor.execute(sqlquery)
    rows = cursor.fetchall()

    if rows:
        df = pd.read_sql(sqlquery, conn)

        # Anzahl Tabs = Anzahl Jahre in DF
        num_tabs = len(df)

        # Tabs erstellen
        tab_titles = [f'Jahr {year}' for year in df['Year'].tolist()[:num_tabs]]
        tabs = st.tabs(tab_titles)

        # Checkboxes dem jeweiligen Tab hinzufügen
        for i, year in enumerate(df['Year'].tolist()[:num_tabs]):
            with tabs[i]:
                conn = mysql.connector.connect(**connex())
                sql_query = f"""
                SELECT * FROM `main_quick_data` WHERE YEAR(datum) = {year} AND user = {user} ORDER BY `datum` ASC
                """
                df = pd.read_sql(sql_query, conn)
                df = df.drop(columns=['id','user'])
                df = df.sort_values('datum') 
                df['quick'] = df['quick'].astype(float)  
                df = df.sort_values(by=['datum', 'quick'],ascending=False) 
                df['checkbox'] = df.index

                conn.commit()
                conn.close()

                num_checks = len(df)
                num_cols = (num_checks // 25) + (num_checks % 25 > 0)
                cols = st.columns(num_cols)

                with st.form(key=f'loeschen{i}'):
                    checked_boxes = {}
                    for i, row in df.iterrows():
                        with cols[i % num_cols]:
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
                    #if alles:
                    #   nichtgewählte = [key for key, checked in checked_boxes.items() if not checked]
                    #  st.success(nichtgewählte)
                    # for state in nichtgewählte:
                        #    st.session_state[f'{state}'] = True
                        #   st.write(st.session_state[f'{state}'])
                        