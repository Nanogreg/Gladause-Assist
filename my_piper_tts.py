import io, wave, numpy, sounddevice
from piper import PiperVoice
from piper_voice_model import get_voice_by_name
from pathlib import Path

class VoiceSession:
    """A VoiceSession object is keeping the custom voice model (PiperVoiceModel) and onnx model in memory.

    Attributes:
        voice_name (str): The name of the voice model to use. Default to 'Gladause'
        onnx_model : The onnx model is loaded automaticly according to the voice name provided.
    """
    def __init__ (self, voice_name: str = 'Gladause'):
        self.model = get_voice_by_name(voice_name)
        if(self.model):
            try:
                self.onnx_model = PiperVoice.load(Path('voices') / self.model.file_name)
            except Exception as e:
                print(f'❌ Error loading the model : {e}')
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
        voice_session.onnx_model.synthesize_wav(text, wav_file, syn_config=getattr(voice_session.model, 'config'))

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