import streamlit as st
import pandas as pd
from shillelagh.backends.apsw.db import connect
import pyqrcode
import png
from PIL import Image

connection = connect(":memory:")
cursor = connection.cursor()
title = 'Gereja Santa Maria Imakulata'
excel = pd.read_excel("DataLingkungan-20230324.xlsx")

st.set_page_config(page_title=title, layout="centered")

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

c1, c2, c3 = st.columns(3)
kode_wilayah = c1.selectbox("Kode Wilayah", read_wilayah())
kode_lingkungan = c2.selectbox("Kode Lingkungan", read_lingkungan(kode_wilayah))
nama_lingkungan = c3.text_input("Nama Lingkungan", value=read_nama(kode_wilayah, kode_lingkungan).iat[0, 0], disabled=True)
    
c4, c5 = st.columns(2)
user_name = c4.text_input("Nama")
user_phone = c5.text_input("Nomor Telepon")
submit = st.button("Kirim")
    
if submit:
    if user_phone[0] == "0":
        user_phone = user_phone.replace('0', '+62', 1)
    img_title = str(kode_lingkungan) + "_" + user_name
    qr_code = pyqrcode.create(img_title)
    loc = "img/{img_title}.png".format(img_title = img_title)
    qr_code = qr_code.png(loc, scale = 6)

    c6, c7, c8 = st.columns(3)
    image = Image.open(loc)
    c7.write("Mohon Download atau Screenshot QR Code dibawah")
    c7.image(image)
    c7.download_button("Download QR", data=open(loc, 'rb').read(), file_name=img_title+".png", mime='image/png')
