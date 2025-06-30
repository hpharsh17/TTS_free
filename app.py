from flask import Flask, request, render_template
import pyttsx3
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)


def send_email(recipient, filepath):
    """Send the generated audio file to the given email address."""
    msg = EmailMessage()
    msg["Subject"] = "Your TTS Audio File"
    msg["From"] = "noreply@example.com"
    msg["To"] = recipient
    msg.set_content("Please find the generated audio file attached.")

    with open(filepath, "rb") as f:
        data = f.read()
        msg.add_attachment(
            data,
            maintype="audio",
            subtype="wav",
            filename=os.path.basename(filepath),
        )

    try:
        with smtplib.SMTP("localhost") as smtp:
            smtp.send_message(msg)
    except Exception as exc:
        return str(exc)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    error = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        gender = request.form.get('gender', 'male')
        language = request.form.get('language', 'en')
        email = request.form.get('email', '').strip()
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

                def voice_matches(v, lang, gen):
                    voice_gender = str(getattr(v, 'gender', '')).lower()
                    langs = []
                    for l in getattr(v, 'languages', []):
                        if isinstance(l, bytes):
                            l = l.decode('utf-8')
                        langs.append(str(l).split('_')[0].lower())
                    return gen in voice_gender and lang.lower() in langs

                def voice_matches_lang(v, lang):
                    langs = []
                    for l in getattr(v, 'languages', []):
                        if isinstance(l, bytes):
                            l = l.decode('utf-8')
                        langs.append(str(l).split('_')[0].lower())
                    return lang.lower() in langs

                selected_voice = None
                for v in voices:
                    if voice_matches(v, language, gender):
                        selected_voice = v
                        break
                if not selected_voice:
                    for v in voices:
                        if voice_matches_lang(v, language):
                            selected_voice = v
                            break
                if not selected_voice:
                    selected_voice = voices[0]

                engine.setProperty('voice', selected_voice.id)
                if not os.path.exists('static'):
                    os.makedirs('static')
                filepath = os.path.join('static', 'output.wav')
                engine.save_to_file(text, filepath)
                engine.runAndWait()
                audio_file = filepath
                if email:
                    mail_error = send_email(email, filepath)
                    if mail_error:
                        error = f"Failed to send email: {mail_error}"
    return render_template('index.html', audio_file=audio_file, error=error)

if __name__ == '__main__':
    app.run(debug=True)
