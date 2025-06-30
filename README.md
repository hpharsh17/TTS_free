# TTS_free

A simple web interface that converts user provided text to speech using the
open‑source [Coqui TTS](https://github.com/coqui-ai/TTS) library.
The web page now uses [Bootstrap](https://getbootstrap.com/) for a cleaner UI.

The interface now lets you choose the language (English, Spanish, French, German,
Gujarati, Hindi, Arabic, Chinese, Japanese, Korean, Russian, Italian,
Portuguese or Dutch)
and the gender of the voice (male or female).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
The models are downloaded automatically on first run so internet access may be
required the first time you generate speech.

2. Run the application:
   ```bash
   python app.py
   ```

3. Open `http://localhost:5000` in your browser and enter text to generate the audio file.
