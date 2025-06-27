from flask import Flask, request, render_template
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        language = request.form.get('language', 'en')
        voice = request.form.get('voice', 'com')
        if text:
            tts = gTTS(text=text, lang=language, tld=voice)
            if not os.path.exists('static'):
                os.makedirs('static')
            filepath = os.path.join('static', 'output.mp3')
            tts.save(filepath)
            audio_file = filepath
    return render_template('index.html', audio_file=audio_file)

if __name__ == '__main__':
    app.run(debug=True)
