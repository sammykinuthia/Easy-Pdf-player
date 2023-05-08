from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from PyPDF2 import PdfReader
from io import BytesIO
import os
import pyttsx3 as pt
from threading import Thread
from gtts import gTTS
import time



app = Flask(__name__,  static_folder='media/')
CORS(app)

engine = pt.init()



path = ''
@app.route('/', methods=['GET', "POST"])
def index():
    audios = get_audios()
    if request.method == "POST":
        try:
            f = request.files['pdf_file']
            file_name = os.path.splitext(f.filename)[0]
            global path
            path = f'media/audio/{file_name}.wav'
            f.save(f'media/pdfs/{file_name}.pdf')
            create_audio(file_name)
            file_path = os.path.join(os.getcwd(), 'media/audio/'+file_name+".mp3")
            return jsonify(status=201, audio=file_path)
        except Exception:
            print(Exception.mro)
            return jsonify(error=Exception.with_traceback, audios=audios)
   
    return jsonify(status=200, audios=audios)



def create_audio(file_name):
    with open(f"media/pdfs/{file_name}.pdf",'rb') as fb:
        stream = BytesIO(fb.read())
    viewer = PdfReader(stream)
    text = " ".join([page.extract_text() for page in viewer.pages])
    text = " ".join(text.splitlines())
    file_path = os.path.join(os.getcwd(), 'media/audio/'+file_name+".mp3")
    try:
        audio = gTTS(text)
        audio.save(file_path)
    except Exception as e:
        print(e)
    # engine.save_to_file(text, file_path)
    # engine.runAndWait()



@app.route('/wav')
def stream(path=path):
    def generate():
        with open(path,'rb') as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)
    return Response(generate(), mimetype='audio/x-wav')



def get_audios():
    audio_path = os.path.join(os.getcwd()+'/media/audio')
    audio_list = os.listdir(audio_path)
    audios = {}
    if len(audio_list) > 0:
        for item in audio_list:
            audios[item] = 'media/audio/'+item
    return audios


if __name__=="__main__":
    app.run(debug=True, port=9090)