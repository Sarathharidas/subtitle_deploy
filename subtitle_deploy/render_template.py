from flask import Flask, render_template, url_for, request, redirect, url_for
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import youtube_dl

import requests
from datetime import timedelta


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
  txt_file = whisper_api(new_video.wav)
  return send_file(txt_file, as_attachment=True)

def whisper_api(audio_wav):
  url = "https://transcribe.whisperapi.com"
  headers = {
'Authorization': 'Bearer 3G32WTPNZ7F3YGQNYAQ4GFYJLY81UH9B'
}
  file = {'file': open(audio_wav, 'rb')}
  data = {

  "diarization": "false",
  #Note: setting this to be true will slow down results.
  #Fewer file types will be accepted when diarization=true
  #"numSpeakers": "2",
  #if using diarization, you can inform the model how many speakers you have
  #if no value set, the model figures out numSpeakers automatically!
   #can't have both a url and file sent!, 
   "task":"translate"
}
response = requests.post(url, headers=headers, files=file, data=data)
print(response.text)

response_json = response.json()
segments = response_json['segments']

for segment in segments:
  startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
  endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
  text = segment['text']
  segmentId = segment['id']+1
  segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

  srtFilename = os.path.join("SrtFiles", f"VIDEO_FILENAME.srt")
  with open(srtFilename, 'a', encoding='utf-8') as srtFile:
    srtFile.write(segment)



if __name__ == '__main__':
  app.debug
  app.run()