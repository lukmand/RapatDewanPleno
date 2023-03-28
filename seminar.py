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

def format_func(option):
    return lingkungan_dict[option]

def read_wilayah():

    query = "select distinct kode_wilayah from excel"
    query_res = cursor.execute(query).fetchall()
    df  = pd.DataFrame.from_records(query_res, columns = [column[0] for column in cursor.description])

    return df
    
def read_lingkungan(kode_wilayah):

    query = "select distinct case when length(kode_lingkungan) = 3 then '0' || kode_lingkungan else kode_lingkungan end kode_lingkungan, nama_lingkungan from excel where kode_wilayah = {kode_wilayah}".format(kode_wilayah = kode_wilayah)
    query_res = cursor.execute(query).fetchall()
    df  = pd.DataFrame.from_records(query_res, columns = [column[0] for column in cursor.description])
    #print(df)
    return df
    
    
st.write("# Rapat Dewan Pleno")    

c1, c2 = st.columns(2)
lingkungan_dict = {}
kode_wilayah = c1.selectbox("Kode Wilayah", read_wilayah())
lingkungan_df = read_lingkungan(kode_wilayah)
for i in lingkungan_df.values.tolist():
    lingkungan_dict[i[0]] = i[1]
    
kode_lingkungan = c2.selectbox("Nama Lingkungan", options = list(lingkungan_dict.keys()), format_func = format_func)
    
c4, c5 = st.columns(2)
user_name = c4.text_input("Nama")
user_phone = c5.text_input("Nomor Telepon")
submit = st.button("Kirim")
    
if submit:
    if user_phone[0] == "0":
        user_phone = user_phone.replace('0', '+62', 1)
    img_title = str(kode_lingkungan) + "_" + user_name + "_" + user_phone
    qr_code = pyqrcode.create(img_title)
    loc = "img/{img_title}.png".format(img_title = img_title)
    qr_code = qr_code.png(loc, scale = 6)
    
    c6, c7, c8 = st.columns(3)
    
    c7.write(img_title)
    image = Image.open(loc)
    c7.write("Mohon Download atau Screenshot QR Code dibawah")
    c7.image(image)
    c7.download_button("Download QR", data=open(loc, 'rb').read(), file_name=img_title+".png", mime='image/png')
