import ollama
from my_piper_tts import VoiceSession, generate_voice
from piper_voice_model import get_voice_names
from typing import Any, cast, Dict

# Ollama Gemma Models
gemma4_e4b = 'gemma4:e4b'               # Full e4b model
gemma4_e2b_q4 = 'batiai/gemma4-e2b:q4'  # e2b quantized q4 (fastest)
gemma4_e4b_q4 = 'batiai/gemma4-e4b:q4'  # e4b quantized Q4 (fast)
gemma4_e4b_q6 = 'batiai/gemma4-e4b:q6'  # e4b quantized Q6
gemma4_uncensored = """
mdhm_hmmd/gemma4-e4b-uncensored-q8"""   # e4b uncensored quantized Q8
gemma4_9b = 'gemma2:9b'                 # Bigger 9b model (slow)
default_llm_model = gemma4_e4b_q4

# System configuration for text generation
cpu_cores = 8       # Numer of CPU cores
gpu_offload = 10    # GPU offload : 0 - 99

def start_conversation(voice_name: str = 'Gladaus', stream_conv: bool = True, llm_model_name: str = default_llm_model):
    """Starts a conversation between the user and the AI with text + speach response using Gemma4 and Piper-tts.

    Args:
        stream_conv (bool, optional): Specify if the text and voice are generated in one block or streamed. Defaults to True.
        voice_model (str, optional): Voice model name to use (see: piper_voice_model.py). Defaults to 'Gladaus'(en).
    """
    # Getting the voice model
    voice_session = VoiceSession(voice_name)
    if not voice_session.model:
        print(f"[Gladaus] Error getting the voice model : {voice_name}\n=== Exit ===")
        generate_voice("Error : Cannot load the voice model.")
        return
        
    user = 'Moi' if voice_session.model.lang == 'fr' else 'Me'
    
    # Welcome msg
    welcome_msg = generate_welcome_msg(voice_session, llm_model_name)

    # First conversaion history with system role
    messages = [{'role': 'system','content': voice_session.model.personality}]
    messages.append({
        'role': 'assistant',
        'content': welcome_msg
    })

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
            chunk_dict = cast(Dict[str, Any], chunk)
            content = chunk_dict['message']['content']
            content = content.replace('*','')
            assistant_response += content
            response_part += content
            if(response_part and response_part[-1] in ['.', '?', '!',';']): # sentence by sentence voice generation
                print(response_part, end='', flush=True)
                generate_voice(response_part, voice_session)
                response_part = ''
        print('')
    else:
        response_dict = cast(Dict[str, Any], response_data)
        assistant_response = response_dict['message']['content']
        print(assistant_response)
        generate_voice(assistant_response, voice_session) 
        
    return assistant_response

def check_llm_model(llm_model: str)-> bool:
    """Check If the LLM model name is aviable in ollama try downloading it. 
    If ollama is not running or the model is not aviable, raise an error and return false. 
    
    Args:
        llm_model (str): Ollama LLM model name

    Returns:
        (bool): True if the model is dowloaded locally; False if the model is not downloaded.
    """
    try:
        # List of all aviable models installed locally
        ollama_response = ollama.list()
        model_found = False

        for model in ollama_response.models:
            if model.model == llm_model: model_found = True
           
        # If the provided model is not found then try downloading it 
        if not model_found:
            try:
                # Waiting for download message text + voice
                print(f"[Gladaus] Attempting to download '{llm_model}', please wait...")
                print("[System] ⚠️This process can take a while depending on your internet connection.")
                generate_voice("Attempting to download language model, please wait.")
                
                ollama.pull(llm_model)
                
                # Model loaded message text + voice
                print(f"[Gladaus] LLM '{llm_model}' downloaded.")
                generate_voice("Large language model downloaded successfully.")
                
            except ollama.ResponseError as e:
                print(f"\n[Gladaus] Error : the selected language model was not found. Download failed.")
                generate_voice("Error : the selected language model was not found. Download failed.")
                return False
            
        return True
    # Ollama server is not running
    except Exception as e:
        print("[System] ⚠️ Download and run ollama server first.")
        print("[Gladaus] Error: Cannot connect to Ollama. Is the server running?")
        generate_voice("Error : Cannot connect to Ollama. Is the server running?")
        return False
        

def generate_welcome_msg(voice_session: VoiceSession, llm_model_name: str, ) -> str:
    # Loading message by language
    if getattr(voice_session.model, 'lang') =='fr':
        print("[Gladause] Chargement du modèle de langage, veuillez patienter ... \n")
        generate_voice("Chargement du modèle de langage, veuillez patienter ...", VoiceSession('Gladause')) # Default voice -> Gladause = fr version
    elif getattr(voice_session.model, 'lang') =='en':
        print("[Gladaus] Loading language model into memory, please wait ... \n")
        generate_voice("Loading language model into memory, please wait ...") # Gladaus = en version

    # First welcome message of the assistant
    welcome_msg = [{'role': 'system','content': getattr(voice_session.model, 'welcome_prompt')}]
        
    return process_prompt(welcome_msg, llm_model_name, voice_session, False)

# Setup and starts the conversation    
if __name__ == "__main__": 
    try : 
         # Checking if llm is in ollama or try download it
        if(check_llm_model(default_llm_model)):
            # Chosing voice model
            print(f'[System] Aviable voice models : {get_voice_names()} \n')
            voice_name = input("Choice (ENTER for default): ")
        
            if not voice_name:
                voice_name = 'Gladaus' # Default Gladaus[en]
            print('')
            start_conversation(voice_name=voice_name, llm_model_name=default_llm_model)
    except Exception as e:
        print(f'[System] ❌ Error : {e}')
