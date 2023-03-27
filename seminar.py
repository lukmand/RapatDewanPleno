import streamlit as st
import pandas as pd
from shillelagh.backends.apsw.db import connect
import pyqrcode
from twilio.rest import Client
import png

connection = connect(":memory:")
cursor = connection.cursor()
title = 'Gereja Santa Maria Imakulata'
excel = pd.read_excel("DataLingkungan-20230324.xlsx")

st.set_page_config(page_title=title, layout="centered")

def send_message(user_phone, title, img_title):
    
    account_sid = st.secrets["account_sid"]
    auth_token = st.secrets["auth_token"]
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
      from_='whatsapp:{wa_number}'.format(wa_number = st.secrets["wa_number"]),
      body='This is an automated message for {title}'.format(title = title),
      media_url= "img/{img_title}.png".format(img_title = img_title),
      to='whatsapp:{user_phone}'.format(user_phone = user_phone)
    )

def read_wilayah():

    query = "select distinct kode_wilayah from excel"
    query_res = cursor.execute(query).fetchall()
    df  = pd.DataFrame.from_records(query_res, columns = [column[0] for column in cursor.description])

    return df
    
def read_lingkungan(kode_wilayah):

    query = "select distinct kode_lingkungan from excel where kode_wilayah = {kode_wilayah}".format(kode_wilayah = kode_wilayah)
    query_res = cursor.execute(query).fetchall()
    df  = pd.DataFrame.from_records(query_res, columns = [column[0] for column in cursor.description])

    return df
    
def read_nama(kode_wilayah, kode_lingkungan):

    query = "select distinct nama_lingkungan from excel where kode_wilayah = {kode_wilayah} and kode_lingkungan = {kode_lingkungan}".format(kode_wilayah = kode_wilayah, kode_lingkungan = kode_lingkungan)
    query_res = cursor.execute(query).fetchall()
    df  = pd.DataFrame.from_records(query_res, columns = [column[0] for column in cursor.description])

    return df
    
st.write("# Rapat Dewan Pleno")    
with st.form("my_form", False):    
    c1, c2, c3 = st.columns(3)
    kode_wilayah = c1.selectbox("Kode Wilayah", read_wilayah())
    kode_lingkungan = c2.selectbox("Kode Lingkungan", read_lingkungan(kode_wilayah))
    nama_lingkungan = c3.text_input("Nama Lingkungan", value=read_nama(kode_wilayah, kode_lingkungan).iat[0, 0], disabled=True)
    
    c4, c5 = st.columns(2)
    user_name = c4.text_input("Nama")
    user_phone = c5.text_input("Nomor Telepon")
    submit = st.form_submit_button("Kirim")
    
if submit:
    if user_phone[0] == "0":
        user_phone = user_phone.replace('0', '+62', 1)
    img_title = str(kode_lingkungan) + "_" + user_name
    qr_code = pyqrcode.create(img_title)
    qr_code = qr_code.png("img/{img_title}.png".format(img_title = img_title))

    send_message(user_phone, title, img_title)