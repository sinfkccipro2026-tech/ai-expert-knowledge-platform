"""Speech-to-Text Processing"""
import speech_recognition as sr

class SpeechProcessor:
    """Process speech input"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def transcribe_audio(self, audio_file_path):
        """Transcribe audio file to text"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return {'text': text, 'success': True}
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def transcribe_microphone(self, duration=10):
        """Transcribe from microphone"""
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=duration)
                text = self.recognizer.recognize_google(audio)
                return {'text': text, 'success': True}
        except Exception as e:
            return {'error': str(e), 'success': False}
