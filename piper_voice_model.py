from piper import SynthesisConfig

class PiperVoiceModel:
    def __init__(self, name: str, file_name: str, lang: str, gender: str, config: SynthesisConfig):
        self.name = name
        self.file_name = file_name
        self.lang = lang
        self.gender = gender
        self.config = config
    
def get_voices() -> list[PiperVoiceModel]:
    """Seeds and returns all default voices

    Returns:
        list[PiperVoiceModel]: all seeded voices
    """
    response: list[PiperVoiceModel] = []
    
    response.append(PiperVoiceModel(
        name = 'Gladause',
        file_name = 'fr_FR-glados-medium.onnx',
        lang = 'fr',
        gender = 'robot',
        config = SynthesisConfig(
            volume = 1.0,           # Loudness default 1.0
            length_scale = 1.0,     # Speed default 1.0
            noise_scale = 0.0,      # more audio variation defult 0.667
            noise_w_scale = 1.5,    # more speaking variation default 0.8
            normalize_audio = False,# use raw audio from voice
        )
    ))
    response.append(PiperVoiceModel(
        name = 'Tom',
        file_name = 'fr_FR-tom-medium.onnx',
        lang = 'fr',
        gender = 'male',
        config = SynthesisConfig(
            volume = 1.0,
            length_scale = 1.0,
            noise_scale = 0.65,
            noise_w_scale = 0.8,
            normalize_audio = True,
        )
    ))
    response.append(PiperVoiceModel(
        name = 'Siwi',
        file_name = 'fr_FR-siwis-medium.onnx',
        lang = 'fr',
        gender = 'female',
        config = SynthesisConfig(
            volume = 1.0,
            length_scale = 1.0,
            noise_scale = 0.65,
            noise_w_scale = 0.8,
            normalize_audio = True,
        )
    ))
    response.append(PiperVoiceModel(
        name = 'Jessica',
        file_name = 'fr_FR-upmc-medium.onnx',
        lang = 'fr',
        gender = 'female',
        config = SynthesisConfig(
            volume = 1.0,
            length_scale = 1.0,
            noise_scale = 0.65,
            noise_w_scale = 0.8,
            normalize_audio = True,
        )
    ))
    return response

def get_voice_by_name(name: str) -> PiperVoiceModel | None :
    """Returns a voice model by its name (model.name)

    Args:
        name (str): The model name (starts with Uppercase letter. Example : 'Tom')

    Returns:
        PiperVoiceModel | None: Return the voice model object
    """
    response = [voice for voice in get_voices() if voice.name == name]
    return response[0] if response else None

def get_voice_names() -> list[str]:
    """Returns a list of all available voice model names.

    Returns:
        list[str]: List of all model names
    """
    return [f"{voice.name}[{voice.lang}][{voice.gender}]" for voice in get_voices()]
