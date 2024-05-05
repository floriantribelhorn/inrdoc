import streamlit as st

def connex():
    cnxn_str = {
        'user': st.secrets.db_credentials.user,
        'password': st.secrets.db_credentials.password,
        'host': st.secrets.db_credentials.host,
        'database': st.secrets.db_credentials.database,
        'port': st.secrets.db_credentials.port,
        'auth_plugin': st.secrets.db_credentials.auth_plugin
        }
    return cnxn_str