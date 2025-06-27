from flask import Flask, request, render_template, send_from_directory, url_for
from gtts import gTTS
from gtts.lang import tts_langs
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    languages = tts_langs()
    audio_url = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        lang = request.form.get('lang', 'en')
        if text:
            tts = gTTS(text=text, lang=lang)
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join('static', filename)
            tts.save(filepath)
            audio_url = url_for('static', filename=filename)
    return render_template('index.html', languages=languages, audio_url=audio_url)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('static', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
