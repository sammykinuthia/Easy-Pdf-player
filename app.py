from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from PyPDF2 import PdfReader
from io import BytesIO
from gtts import gTTS
import pyttsx3



app = Flask(__name__,  static_folder='media/')
CORS(app)

path = ''
@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == "POST":
        f = request.files['pdf_file']
        file_name = f.filename
        global path
        path = f'media/audio/{file_name}.wav'
        f.save(f'media/pdfs/{file_name}.pdf')
        with open(f"media/pdfs/{file_name}.pdf",'rb') as fb:
            stream = BytesIO(fb.read())
        viewer = PdfReader(stream)
        text = viewer.pages[0].extract_text()
        
        try:
            # pytts = pyttsx3.Engine()
            # pytts.save_to_file(text, path)
            tts = gTTS(text, lang="en")
            tts.save(path)
            return jsonify(isSuccess=True)
        except Exception:
            print(Exception.mro)
            return jsonify(error=Exception.with_traceback)
   
    return jsonify(ok='okey')


@app.route('/wav')
def stream():
    def generate():
        with open(path,'rb') as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)
    return Response(generate(), mimetype='audio/x-wav')



if __name__=="__main__":
    app.run(debug=True)