from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from threading import Thread
import os
import gspread

app = Flask(__name__)

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt'}
gc = gspread.service_account(filename='serviceAuth.json')

def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  global paper
  if request.method == 'POST':
    # Check if file is uploaded
    if 'textfile' not in request.files:
      return redirect(request.url)
    file = request.files['textfile']
    # Check if file is selected
    if file.filename == '':
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(UPLOAD_FOLDER, filename))
      with open("test.txt", "r") as file:
        text = file.read()
        paper = text.split("\n\n")
        with open("arrays.py",'w') as file1:
          file1.write(f"paper = {paper}")
        range = ["B1","B2","B3","B4","B5","B6","B7","B8"]
        value = ""
        wks = gc.open('smts').sheet1
        for cell in range:
          wks.update([[value]],cell)
      return 'File uploaded successfully!'
  return render_template('upload.html')

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()