import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mysql.connector
import plotly.graph_objects as go
import time

cnxn_str = {
    'user': st.secrets.db_credentials.user,
    'password': st.secrets.db_credentials.password,
    'host': st.secrets.db_credentials.host,
    'database': st.secrets.db_credentials.database,
    'port': st.secrets.db_credentials.port,
    'auth_plugin': st.secrets.db_credentials.auth_plugin
}

def quick_data_check(user, dauer):
    conn = mysql.connector.connect(**cnxn_str)
    sql_query = f"""
    SELECT * FROM `freedb_inrdoc`.`main_quick_data` WHERE user = {user} ORDER BY `datum` ASC
    """

    df = pd.read_sql(sql_query, conn)
    df = df.drop(columns=['id','user'])
    df = df.sort_values('datum') 
    df['quick'] = df['quick'].astype(float)  
    df = df.sort_values(by=['datum', 'quick'],ascending=False)  
    df = df.head(dauer)    

    fig = go.Figure(data=go.Scatter(x=df['datum'], y=df['quick'], mode='lines'))
    cursor = conn.cursor()
    cursor.execute('SELECT `vorname` FROM `freedb_inrdoc`.`user_data` WHERE id = %s', (user,))
    rows = cursor.fetchall()

    fig.update_layout(
        xaxis=dict(title='Datum', tickformat='%Y-%m-%d'),
        yaxis=dict(title='Quick'),
        title=f'Quick Daten von {rows[0][0]} letzte {dauer} Dateneinträge',
    )

    st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")
    conn.commit()
    conn.close()

def quick_empty(user, date):
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute(f'SELECT `datum` FROM `freedb_inrdoc`.`main_quick_data` WHERE datum = %s AND user = %s', (date,user,))
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
    id = st.session_state['loggedinuserid']
    cursor.execute(f'SELECT `med` FROM `freedb_inrdoc`.`user_data` WHERE id = %s', (id,))
    rows = cursor.fetchall()
    med = rows[0][0]
    conn.commit()
    conn.close()

    if rows[0][0] != 0:
        med2 = rows[0][0]
        conn = mysql.connector.connect(**cnxn_str)
        cursor = conn.cursor()
        currentuserid = st.session_state['loggedinuserid']
        cursor.execute(f"""
            INSERT INTO `freedb_inrdoc`.`main_quick_data` (quick, datum, user, medi)
            VALUES (%s,%s,%s,%s)
            """, (quick,date,st.session_state['loggedinuserid'],med2))
        conn.commit()
        conn.close()

        progress_text = "Quick wird gespeichert"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()

        conn = mysql.connector.connect(**cnxn_str)
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT `quick` from `freedb_inrdoc`.`main_quick_data` WHERE datum = %s AND user = %s""", (date,id))
        rows = cursor.fetchall()
        if rows:
            date1 = date.strftime('%d-%m-%Y')
            st.success(f'Quick vom {date1} wurde gespeichert!')
        conn.commit()
        conn.close()
    else:
        st.info('Sie haben noch kein Medikament in Ihrem Profil erfasst!')

def loeschen_eintraege(daten,user):
    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    cursor.execute(f"""
        DELETE FROM `freedb_inrdoc`.`main_quick_data` WHERE datum = %s AND user = %s""", (daten,user,))
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
    alles = st.checkbox(label='Alles auswählen')
    conn = mysql.connector.connect(**cnxn_str)
    sqlquery = f"""
    SELECT YEAR(`datum`) AS Year, COUNT(*) AS Count
    FROM `main_quick_data`
    WHERE user = {user}
    GROUP BY Year
    ORDER BY Year ASC;
    """
    df = pd.read_sql(sqlquery, conn)

    # Anzahl Tabs = Anzahl Jahre in DF
    num_tabs = len(df)

    # Tabs erstellen
    tab_titles = [f'Jahr {year}' for year in df['Year'].tolist()[:num_tabs]]
    tabs = st.tabs(tab_titles)

    # Checkboxes dem jeweiligen Tab hinzufügen
    for i, year in enumerate(df['Year'].tolist()[:num_tabs]):
        with tabs[i]:
            conn = mysql.connector.connect(**cnxn_str)
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
                        checked_boxes[row['datum']] = st.checkbox(label=f":blue[Datum]: {row['datum']} - :orange[Quick]: {row['quick']}", key=f'value_from_{row["datum"]}')
                        if f'value_from_{row["datum"]}' not in st.session_state:
                            st.session_state[f'value_from_{row["datum"]}'] = False
                submit_button = st.form_submit_button(label='Einträge :red[LÖSCHEN]')
                if submit_button:
                        selected_dates = [date for date, checked in checked_boxes.items() if checked]
                        for row in selected_dates:
                            loeschen_eintraege(row,st.session_state['loggedinuserid'])
                        else:
                            st.rerun()
                if alles:
                    nichtgewählte = [key for key, checked in checked_boxes.items() if not checked]
                    st.success(nichtgewählte)
                    for state in nichtgewählte:
                        st.session_state[f'{state}'] = True
                        st.write(st.session_state[f'{state}'])
                        