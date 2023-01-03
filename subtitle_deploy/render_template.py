from flask import Flask, render_template, url_for, request, redirect, url_for
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import youtube_dl

UPLOAD_FOLDER = '/upload_video'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False, 
        'outtmpl':'new_video.wav'
    }
  
@app.route('/')
def landing_page():
    return render_template('landing_page_2.html')

@app.route('/submit', methods=['POST'])
def handle_form_submissione():
  email_address = request.form.get('email')
  print(email_address)
  with open('emails.txt', 'a') as f:
    f.write(email_address + ','+ str(datetime.now())+'\n')
  return render_template('options.html')

# @app.route('/upload',  methods=['POST', 'GET'])
# def upload():
#     if request.method == 'POST':
#         # check if the post request has the file part
#       if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#       file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#       if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
#       if file:
#         filename = secure_filename(file.filename)
#         print("This is the file")
#         print(filename)
#         #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return render_template('landing_page_2.html')

@app.route('/youtube',  methods=['POST', 'GET']) 
def youtube():
  youtube_link = request.form.get('youtube_link')
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([youtube_link])

if __name__ == '__main__':
  app.debug
  app.run()