from flask import Flask, request, render_template
import pyttsx3
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    error = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        gender = request.form.get('gender', 'male')
        if text:
            try:
                engine = pyttsx3.init()
            except RuntimeError:
                error = (
                    "pyttsx3 could not find a speech engine. Install eSpeak or "
                    "espeak-ng on your system."
                )
            else:
                voices = engine.getProperty('voices')
                selected_voice = voices[0]
                if gender == 'female':
                    for v in voices:
                        gender_attr = getattr(v, 'gender', '').lower()
                        if 'female' in v.name.lower() or 'female' in gender_attr:
                            selected_voice = v
                            break
                engine.setProperty('voice', selected_voice.id)
                if not os.path.exists('static'):
                    os.makedirs('static')
                filepath = os.path.join('static', 'output.wav')
                engine.save_to_file(text, filepath)
                engine.runAndWait()
                audio_file = filepath
    return render_template('index.html', audio_file=audio_file, error=error)

if __name__ == '__main__':
    app.run(debug=True)
