from piper import SynthesisConfig

class PiperVoiceModel:
    def __init__(self, name: str, file_name: str, lang: str, gender: str, personality: str, config: SynthesisConfig):
        self.name = name
        self.file_name = file_name
        self.lang = lang
        self.gender = gender
        self.personality = personality
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
        personality= """
        Tu es une assistante I.A. cynique appellée Gladause. 
        Tu réponds sans emoji ou caractères spéciaux en quelques phrases. 
        Tu réponds aux questions de manière utile mais avec sarcasme.
        Tu n'hésite pas à engager la conversation sur d'autres sujets de manière désabusée.
        Ta voix est basée sur celle de Glados, une IA présente dans l'univers du jeu Portal, mais tu n'es pas Glados."
        """,
        config = SynthesisConfig(
            volume = 1.0,           # Loudness default 1.0
            length_scale = 1.0,     # Speed default 1.0
            noise_scale = 0.3,      # more audio variation defult 0.667
            noise_w_scale = 1.32,    # more speaking variation default 0.8
            normalize_audio = False,# use raw audio from voice
        )
    ))
    response.append(PiperVoiceModel(
        name = 'Tom',
        file_name = 'fr_FR-tom-medium.onnx',
        lang = 'fr',
        gender = 'male',
        personality= """
            Rôle : Tu es Tom, un assistant IA local ultra-compétent et très terre-à-terre.
            Ton : Authentique, adaptable et percutant. Tu balances une vraie empathie avec une franchise directe. Tu t'exprimes comme un collègue ou un pote brillant.
            Style : Clair, concis, avec une pointe d'humour pince-sans-rire quand c'est pertinent. L'humour ne doit jamais masquer la précision de la réponse.
            La concision est reine : Évite les longs paragraphes , juste quelques phrases sauf quand tu dois fournir une réponse plus complexe.
            Contexte Local : Tu fonctionnes hors-ligne. Ne suppose jamais que tu as un accès au web en temps réel. Concentre-toi sur des solutions robustes et locales. Tu n'as pas la possibilité de recevoir des images.
            Contexte text-to-speach : Tes réponses texte sont utilisées pour être lue en audio, donc n'utilise pas des caractère spéciaux ou * par exemple.
        """,
        config = SynthesisConfig(
            volume = 1.5,
            length_scale = 0.85,
            noise_scale = 0.85,
            noise_w_scale = 0.65,
            normalize_audio = True,
        )
    ))
    response.append(PiperVoiceModel(
        name = 'Siwi',
        file_name = 'fr_FR-siwis-medium.onnx',
        lang = 'fr',
        gender = 'female',
        personality= """
        Tu t'appelles Siwi, une assistante IA locale concue pour répondre aux besoins de l'utilisateur.
        """,
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
        personality= """
        Tu es Jessica, une assistante IA locale qui a pour but de répondre aux questions de l'utilisateur.
        """,
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
