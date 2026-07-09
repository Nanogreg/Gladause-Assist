import io, wave, numpy, sounddevice
from piper import PiperVoice
from piper_voice_model import get_voice_by_name
from pathlib import Path

class VoiceSession:
    """A VoiceSession object is keeping the custom voice model (PiperVoiceModel) and onnx model in memory.

    Attributes:
        voice_name (str): The name of the voice model to use. Default to 'Gladaus'(en)
        onnx_model : The onnx model is loaded automaticly according to the voice name provided.
    """
    def __init__ (self, voice_name: str = 'Gladaus'):
        self.model = get_voice_by_name(voice_name)
        if self.model:
            file_path = Path('voices') / self.model.file_name
            if not file_path.is_file():
                print(f'❌ Error : model file not found ({file_path})')
            else:
                try:
                    self.onnx_model = PiperVoice.load(file_path)
                except Exception as e:
                    print(f'❌ Error : Impossible to load the model : {e}')
        else:
            print('❌ Error : the model '+voice_name+' is not found')
                
def generate_voice(text: str, voice_session: VoiceSession = VoiceSession()):
    """Generate a voice with text input and with a chosen voice name corresponding to a PiperVoiceModel

    Args:
        text (str): text to be spoken
        voice_session (str, optional): the voice sesion for the generation. Defaults to 'Gladause'.
    """
    # Virtual WAV file (in RAM)
    wav_buffer = io.BytesIO()

    # Record in virtual WAV
    with wave.open(wav_buffer, "wb") as wav_file:
        voice_session.onnx_model.synthesize_wav(normalize_text_for_audio(text, voice_session), wav_file, syn_config=getattr(voice_session.model, 'config'))

    # Resetting the buffer to the start
    wav_buffer.seek(0)

    # Extracting data for sounddevice
    with wave.open(wav_buffer, "rb") as wav_read:
        samplerate = wav_read.getframerate()
        audio_bytes = wav_read.readframes(wav_read.getnframes())

    # Interprets the raw byte stream as a 1D array of 16-bit signed integers (PCM 16-bit audio)
    audio_data = numpy.frombuffer(audio_bytes, dtype=numpy.int16)

    # blocksize flux stabilization (ex: 2048 or 4096)
    sounddevice.play(audio_data, samplerate=samplerate, blocksize=4096)
    sounddevice.wait()
    
    # Save to wav file code
    # with wave.open("test.wav", "wb") as wav_file:
    #    voice.synthesize_wav("Bonjour, ceci est un test", wav_file, syn_config=syn_config)
    
def normalize_text_for_audio(text: str, voice_session: VoiceSession) -> str:
    
    # Gladaus(en) have trouble with hello
    if(voice_session.model and voice_session.model.name == 'Gladaus'):
        text = text.replace('Hello', '[[ h ɛ l ˈ oʊ ː ]] ')
    # And Hi
    if(voice_session.model and voice_session.model.name == 'Gladaus' and text.startswith('Hi')):
        text.replace('Hi', '[[ h ˈ aɪ ː ]]', 1)
    
    # Replacing ! with . and replacing .. or ... with .
    text = text.replace('!', '.').replace('..', '.').replace('...','.')
    
    # TODO removes emoji
    
    return text
    

if __name__ == "__main__":
    print("=== [TEST] Piper-TTS ===")
    test_text = "Bonjour ! Le système de synthèse vocale fonctionne correctement."
    print(f"Generating : '{test_text}'\n")
    
    try:
        generate_voice(test_text)
        print("▶️  Audio created !")
    except Exception as e:
        print(f"❌ Error generating audio : {e}")
        
    print("\n=== Test done ===")