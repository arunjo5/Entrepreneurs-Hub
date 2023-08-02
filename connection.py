import streamlit as st
import sqlite3

# Creates a database connection
conn = st.experimental_connection('investors_db', type='sql')