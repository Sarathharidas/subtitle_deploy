from flask import Flask, render_template, url_for, request, redirect, url_for, send_file
from datetime import datetime
from werkzeug.utils import secure_filename
import os
#import youtube_dl
import subprocess
import requests
from datetime import timedelta

Arlington, VirginiaArlington, Virginia
UPLOAD_FOLDER = '/upload_video'Arlington, Virginia

app = Flask(__name__)Ocean City, Maryland
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
  email_path = os.path.join( os.getcwd(), 'emails.txt')
  with open(email_path, 'a') as f:
    f.write(email_address + ','+ str(datetime.now())+'\n')
  return render_template('upload.html')

@app.route('/upload',  methods=['POST', 'GET'])
def upload():
  if request.method == 'POST':
        # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
        # show a message while the file is being uploaded
    #print('file is')
    #print(file)
    #print(file.filename)
    filename = secure_filename(file.filename)
    video_file_only_name = filename[0:filename.find('.')]
    video_folder_path = os.path.join(os.getcwd(), video_file_only_name)
    if not os.path.exists(video_folder_path):
      os.makedirs(video_folder_path)
    video_file_path_full = os.path.join(video_folder_path, filename)
    file.save(os.path.join(video_folder_path, filename))
        # redirect the user to the uploaded file's URL
    wav_file_path = os.path.join(video_folder_path, video_file_only_name+'.wav')
    command = "ffmpeg -i {0} -ab 160k -ac 2 -ar 44100 -vn {1}".format(video_file_path_full, wav_file_path)
    subprocess.call(command, shell=True)
    srtFilename = whisper_api(wav_file_path, video_folder_path)
    os.remove(video_file_path_full)
    os.remove(wav_file_path)
    return send_file(srtFilename, as_attachment=True)



def whisper_api(audio_wav_path, video_folder_path):
  url = "https://transcribe.whisperapi.com"
  headers = {
'Authorization': 'Bearer 3G32WTPNZ7F3YGQNYAQ4GFYJLY81UH9B'  
}
  file = {'file': open(audio_wav_path, 'rb')}
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
  #print(response.text)

  response_json = response.json()
  segments = response_json['segments']
  segmentId = 0
  for segment in segments:
    startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
    endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
    text = segment['text']
    segmentId = segmentId +1
    segment_text = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

    srtFilename = os.path.join(video_folder_path, 'english_subtitles.srt')
    with open(srtFilename, 'a', encoding='utf-8') as srtFile:
      srtFile.write(segment_text) 
  return srtFilename

# @app.route('/youtube',  methods=['POST', 'GET']) 
# def youtube():
#   youtube_link = request.form.get('youtube_link')
#   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     ydl.download([youtube_link])
#   srtFilename = whisper_api(new_video.wav, youtube_link)
#   os.system( 'rm new_video.wav')
#   return send_file(srtFilename, as_attachment=True)


if __name__ == '__main__':
  app.debug
  app.run()
