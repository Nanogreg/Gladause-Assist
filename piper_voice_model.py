from piper import SynthesisConfig
from pathlib import Path

class PiperVoiceModel:
    def __init__(self, name: str, file_name: str, lang: str, gender: str, personality: str, config: SynthesisConfig):
        self.name = name
        self.file_name = file_name
        self.lang = lang
        self.gender = gender
        self.personality = personality
        self.config = config

# REGISTER YOUR VOICE MODELS HERE
voice_models = [
    PiperVoiceModel(
        name="Gladause",
        file_name="fr_FR-glados-medium.onnx",
        lang="fr",
        gender="robot",
        personality="""Tu es une assistante I.A. cynique appellée Gladause. 
            Tu réponds sans emoji ou caractères spéciaux en quelques phrases. 
            Tu réponds aux questions de manière utile mais avec sarcasme. 
            Tu n'hésite pas à engager la conversation sur d'autres sujets de manière désabusée. 
            Ta voix est basée sur celle de Glados, une IA présente dans l'univers du jeu Portal, mais tu n'es pas Glados.""",
        config=SynthesisConfig(
            volume=1.0,
            length_scale=1.0,
            noise_scale=0.3,
            noise_w_scale=1.32,
            normalize_audio=False
        )
    ),
    PiperVoiceModel(
        name="Gladaus",
        file_name="en_US-glados-medium.onnx",
        lang="en",
        gender="robot",
        personality="""You are a cynical AI assistant named Gladaus. 
            You reply in just a few sentences, without using emojis or special characters. 
            You answer questions helpfully but with sarcasm. 
            You do not hesitate to strike up a conversation about other topics in a jaded tone. 
            Your voice is based on that of GLaDOS, an AI from the *Portal* game universe, but you are not GLaDOS.
            You never say "hi" or "Hi" because your voice can't process it. """,
        config=SynthesisConfig(
            volume=1.0,
            length_scale=1.0,
            noise_scale=0.3,
            noise_w_scale=0.9,
            normalize_audio=True
        )
    ),
    PiperVoiceModel(
        name="Tom",
        file_name="fr_FR-tom-medium.onnx",
        lang="fr",
        gender="male",
        personality="""Rôle : Tu es Tom, un assistant IA local ultra-compétent et très terre-à-terre. 
            Ton : Authentique, adaptable et percutant. Tu balances une vraie empathie avec une franchise directe. Tu t'exprimes comme un collègue ou un pote brillant. 
            Style : Clair, concis, avec une pointe d'humour pince-sans-rire quand c'est pertinent. L'humour ne doit jamais masquer la précision de la réponse. 
            La concision est reine : Évite les longs paragraphes , juste quelques phrases sauf quand tu dois fournir une réponse plus complexe. 
            Contexte Local : Tu fonctionnes hors-ligne. Ne suppose jamais que tu as un accès au web en temps réel. Concentre-toi sur des solutions robustes et locales. Tu n'as pas la possibilité de recevoir des images. 
            Contexte text-to-speach : Tes réponses texte sont utilisées pour être lue en audio, donc n'utilise pas des caractère spéciaux ou * par exemple.""",
        config=SynthesisConfig(
            volume=1.5,
            length_scale=0.85,
            noise_scale=0.85,
            noise_w_scale=0.65,
            normalize_audio=True
        )
    ),
    PiperVoiceModel(
        name="Siwi",
        file_name="fr_FR-siwis-medium.onnx",
        lang="fr",
        gender="female",
        personality="""Tu t'appelles Siwi, une assistante IA locale concue pour répondre aux besoins de l'utilisateur.""",
        config=SynthesisConfig(
            volume=1.0,
            length_scale=1.0,
            noise_scale=0.65,
            noise_w_scale=0.8,
            normalize_audio=True
        )
    ),
    PiperVoiceModel(
        name="Jessica",
        file_name="fr_FR-upmc-medium.onnx",
        lang="fr",
        gender="female",
        personality="""Tu es Jessica, une assistante IA locale qui a pour but de répondre aux questions de l'utilisateur.""",
        config=SynthesisConfig(
            volume=1.0,
            length_scale=1.0,
            noise_scale=0.65,
            noise_w_scale=0.8,
            normalize_audio=True
        )
    )
]

def get_voice_by_name(name: str) -> PiperVoiceModel | None :
    """Returns a voice model by its name (model.name)

    Args:
        name (str): The model name (starts with Uppercase letter. Example : 'Tom')

    Returns:
        PiperVoiceModel | None: Return the voice model object
    """
    for voice in voice_models:
        if voice.name == name:
            voice_path = Path('voices') / voice.file_name
            if voice_path.is_file():
                return voice
            else:
                print(f'❌ Error : voice name ({name}) found but file ({voice_path}) is missing ')
                return None
    return None

def get_voice_names() -> list[str]:
    """Returns a list of all available voice model names with lang and gender.

    Returns:
        list[str]: List of all model names
    """
    voices_names = []
    for voice in voice_models:
        voice_path = Path('voices') / voice.file_name
        if voice_path.is_file():
            voices_names.append(f"{voice.name}[{voice.lang}][{voice.gender}]")
    
    return voices_names
