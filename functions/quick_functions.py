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
    tablename = f'quick_data_from_{user}'
    sql_query = f"""
    SELECT * FROM `freedb_inrdoc`.`{tablename}` ORDER BY `datum` ASC
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
    currentuserid = st.session_state['loggedinuserid']
    tablename = f'quick_data_from_{currentuserid}'
    cursor.execute(f"""
        INSERT INTO `freedb_inrdoc`.`{tablename}` (quick, datum, user)
        VALUES (%s,%s,%s)
        """, (quick,date,st.session_state['loggedinuserid']))
    conn.commit()
    conn.close()

    progress_text = "Quick wird gespeichert"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.03)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    conn = mysql.connector.connect(**cnxn_str)
    cursor = conn.cursor()
    currentuserid = st.session_state['loggedinuserid']
    tablename = f'quick_data_from_{currentuserid}'
    cursor.execute(f"""
        SELECT `quick` from `freedb_inrdoc`.`{tablename}` WHERE datum = %s""", (date,))
    rows = cursor.fetchall()
    if rows:
        date1 = date.strftime('%d-%m-%Y')
        st.success(f'Quick vom {date1} wurde gespeichert!')
    conn.commit()
    conn.close()

def editoranzeige(user,bereich):
        conn = mysql.connector.connect(**cnxn_str)
        tablename = f'quick_data_from_{user}'
        sql_query = f"""
        SELECT * FROM `{tablename}` WHERE YEAR(datum) = {bereich} ORDER BY `datum` ASC
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

