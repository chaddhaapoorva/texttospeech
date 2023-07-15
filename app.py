from flask import Flask, render_template, request
import pyttsx3
import os

app = Flask(__name__)

def get_available_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return voices, engine.getProperty('voice')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
    
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        engine.setProperty('voice', voices[1].id)

        # Convert text to speech
        engine.save_to_file(text, 'static/audio.mp3')
        engine.runAndWait()

        if 'remove_text' in request.form:
            text = ''

        voices, active_voice = get_available_voices()

        return render_template('index.html', text=text, audio_available=True, voices=voices, active_voice=active_voice)

    voices, active_voice = get_available_voices()

    return render_template('index.html', text='', audio_available=False, voices=voices, active_voice=active_voice)

@app.route('/audio')
def audio():
    return app.send_static_file('audio.mp3')

if __name__ == '__main__':
    app.run()
