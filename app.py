from flask import Flask, request, render_template
from TTS.api import TTS
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    error = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        gender = request.form.get('gender', 'male')
        language = request.form.get('language', 'en')
        if text:
            try:
                models = TTS.list_models()
            except Exception as exc:
                error = f"TTS initialization failed: {exc}"
            else:
                model_name = None
                for m in models:
                    if m.startswith(f"tts_models/{language}") and gender.lower() in m.lower():
                        model_name = m
                        break
                if not model_name:
                    for m in models:
                        if m.startswith(f"tts_models/{language}"):
                            model_name = m
                            break
                if not model_name:
                    model_name = "tts_models/en/vctk/vits"

                tts = TTS(model_name)
                if not os.path.exists('static'):
                    os.makedirs('static')
                filepath = os.path.join('static', 'output.wav')
                tts.tts_to_file(text=text, file_path=filepath)
                audio_file = filepath
    return render_template('index.html', audio_file=audio_file, error=error)

if __name__ == '__main__':
    app.run(debug=True)
