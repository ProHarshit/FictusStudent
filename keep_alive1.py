import os
import gspread
from werkzeug.utils import secure_filename
from threading import Thread
import streamlit as st

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt'}
gc = gspread.service_account(filename='serviceAuth.json')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    global paper
    uploaded_file = st.file_uploader("Choose a file", type="txt")
    if uploaded_file is not None:
        text = uploaded_file.getvalue().decode("utf-8")
        paper = text.split("\n\n")
        with open("arrays.py", 'w') as file1:
            file1.write(f"paper = {paper}")
        range = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"]
        value = ""
        wks = gc.open('smts').sheet1
        for cell in range:
            wks.update([[value]], cell)
        st.write('File uploaded successfully!')

def run():
    st.set_page_config(page_title="File Uploader")
    upload_file()

def keep_alive():
    t = Thread(target=run)
    t.start()