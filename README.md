# TTS_free

A simple web interface that converts user provided text to speech using `pyttsx3`.
The web page now uses [Bootstrap](https://getbootstrap.com/) for a cleaner UI.

The interface now lets you choose the language (English, Spanish, French or German)
and the gender of the voice (male or female).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   On Linux, `pyttsx3` relies on an external speech engine. Install
   [eSpeak](https://github.com/espeak-ng/espeak-ng) or `espeak-ng` through
   your package manager if you encounter a `RuntimeError` about missing
   eSpeak.

2. Run the application:
   ```bash
   python app.py
   ```

3. Open `http://localhost:5000` in your browser and enter text to generate the audio file.
