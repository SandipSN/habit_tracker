from deta import Deta
import streamlit as st

DETA_KEY = st.secrets["DETA_KEY_1"]

deta = Deta(DETA_KEY)

db = deta.Base("ld_db")

def insert_record(date, rc):
    return db.put({
        "key": date,
        "rcs": rc
        })

def get_record(date):
    return db.get(date)

def fetch_all():
    res = db.fetch()
    return res.items


