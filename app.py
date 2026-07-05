import ollama
from my_piper_tts import VoiceSession, generate_voice
from piper_voice_model import get_voice_by_name, get_voice_names

# Ollama Gemma Models
gemma4_e4b = 'gemma4:e4b'               # Full e4b model
gemma4_e4b_q4 = 'batiai/gemma4-e4b:q4'  # e4b quantized Q4 (faster)
gemma4_e4b_q6 = 'batiai/gemma4-e4b:q6'  # e4b quantized Q6
gemma4_uncensored = """
mdhm_hmmd/gemma4-e4b-uncensored-q8"""   # e4b uncensored quantized Q8
gemma4_9b = 'gemma2:9b'                 # Bigger 9b model (slower)

# System configuration for text generation
cpu_cores = 8       # Numer of CPU cores
gpu_offload = 10    # GPU offload : 0 - 99

def start_conversation(voice_name: str = 'Gladause', stream_conv: bool = True, llm_model_name: str = 'batiai/gemma4-e4b:q4'):
    """Starts a conversation between the user and the AI with text + speach response using Gemma4 and Piper-tts.

    Args:
        stream_conv (bool, optional): Specify if the text and voice are generated in one block or streamed. Defaults to True.
        voice_model (str, optional): Voice model name to use (see: piper_voice_model.py). Defaults to 'Gladause'.
    """
    
    #Model preload --> !!! to fix
    #ollama.pull(model_name)
    #ollama.chat(model=model_name, keep_alive="10m")
    
    # Getting the voice model
    voice_session = VoiceSession(voice_name)
    if not voice_session.model:
        print(f"Error getting the voice : {voice_name}\n=== Exit ===")
        generate_voice("Erreur de chargement de la configuration.")
        return
        
    user = 'Moi' if voice_session.model.lang == 'fr' else 'Me'
    
    # Welcome msg
    generate_welcome_msg(voice_session, llm_model_name)

    # First conversaion history with system role
    messages = [{'role': 'system','content': voice_session.model.personality}]

    # First prompt out of the loop to handle quit at 1st msg
    user_prompt = input(f'\n[{user}] ').strip()

    while True:
        if user_prompt.strip().lower() in ['exit', 'quit', 'end', 'quitter', 'fin']:
            break
        
        # Adding user prompt to the conv history
        messages.append({
            'role': 'user', 
            'content': user_prompt
        })

        # Adding assistant response to the conv history
        messages.append({
            'role': 'assistant',
            'content': process_prompt(messages, llm_model_name, voice_session, stream_conv)
        })
        
        user_prompt = input(f'\n[{user}] ').strip()
        
def process_prompt(messages, llm_model_name: str, voice_session: VoiceSession , stream_conv: bool) -> str :
    # Getting text response
    response_data  = ollama.chat(
        model=llm_model_name,
        messages=messages,
        think=False,
        stream=stream_conv,
        options={
            'num_ctx': 2048,            # Reduces memory overhead significantly
            'num_predict': 512,         # Limits maximum length of the response
            'num_thread': cpu_cores,    # CPU cores
            'num_gpu' : gpu_offload     # Offload to gpu
        },
    )
    # Printing assistant name
    print(f'\n[{voice_name}] ', end='')

    if(stream_conv):
        assistant_response = '' # Full response
        response_part = ''      # Part of the full response
        for chunk in response_data:
            content = chunk['message']['content'] # type: ignore
            content = content.replace('*','')
            assistant_response += content
            response_part += content
            if(response_part and response_part[-1] in ['.', '?', '!',';']): # sentence by sentence voice generation
                print(response_part, end='', flush=True)
                generate_voice(response_part, voice_session)
                response_part = ''
        print('')
    else:
        assistant_response = response_data['message']['content'] # type: ignore
        print(assistant_response)
        generate_voice(assistant_response, voice_session) 
        
    return assistant_response

def generate_welcome_msg(voice_session: VoiceSession, llm_model_name: str, ):
    welcome_msg_fr = f"Tu es un assistant IA nommé {voice_session.model.name}, ceci est ton tout premier message. tu souhaites bievement la bienvenue à l'utilisateur en une phrase puis lui demande comment tu peux l'aider en une phrase courte également."
    welcome_msg_en = f"You are an AI assistant named {voice_session.model.name}. This is your very first message; briefly welcome the user in one sentence and ask him how you can help him in one short sentence too."
    
    if voice_session.model.lang =='fr':
        print("Chargement du modèle de langage, veuillez patienter ... \n")
        generate_voice("Chargement du modèle de langage, veuillez patienter ...")
        welcome_msg = [{'role': 'system','content': welcome_msg_fr}]
    else:
        print("[System] Loading language model ... \n")
        generate_voice("Loading language model ...")
        welcome_msg = [{'role': 'system','content': welcome_msg_en}]
        
    process_prompt(welcome_msg, llm_model_name, voice_session, False)

# Setup and starts the conversation    
if __name__ == "__main__": 
    print(f'=== Aviable models : {get_voice_names()} ===\n')
    voice_name = input("Choice (ENTER for default): ")
    if not voice_name:
        voice_name = 'Gladause' # Default Gladause[fr]
    print('')
    start_conversation(voice_name=voice_name, stream_conv=True, llm_model_name=gemma4_e4b_q4)
