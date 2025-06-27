from flask import Flask, request, render_template, send_file
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text:
            tts = gTTS(text)
            filepath = 'output.mp3'
            tts.save(filepath)
            return send_file(filepath, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
