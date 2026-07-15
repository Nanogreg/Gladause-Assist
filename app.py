import ollama
from ollama_llm_model import gemma_models, find_or_pull_llm_model
from my_piper_tts import VoiceSession, generate_voice
from piper_voice_model import get_voice_names
from typing import Any, cast, Dict
from hardware_config import HardwareConfig

default_llm_model = gemma_models['gemma4_e2b_q4'] #default E2B_Q4 (fastest)
hardware = HardwareConfig()

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
    system_prompt = [{'role': 'system','content': voice_session.model.personality}]
    messages = system_prompt + [{
        'role': 'assistant',
        'content': welcome_msg
    }]

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

        # The assistant only takes the last 9 messages history (1 to 10) to not overload the memory
        new_msg = process_prompt(system_prompt + messages[1:][-10:], llm_model_name, voice_session, stream_conv)

        # Adding assistant response to the conv history
        messages.append({
            'role': 'assistant',
            'content': new_msg
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
            'num_ctx': hardware.num_ctx,        # Reducing this reduces memory overhead significantly
            'num_predict': -1,                  # Limits maximum length of the response
            'num_thread': hardware.cpu_cores,   # CPU cores
            'num_gpu' : hardware.gpu_offload    # Offload to gpu
        },
    )
    # Printing assistant name
    print(f'\n[{voice_session.model.name if voice_session.model else None}] ', end='')

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


def generate_welcome_msg(voice_session: VoiceSession, llm_model_name: str, ) -> str:
    """Generate a welcome message with the welcome_prompt defined in the voice model

    Args:
        voice_session (VoiceSession): the voice to use
        llm_model_name (str): llm name to use

    Returns:
        str: the welcome message by assistant
    """
    # Loading message by language
    if getattr(voice_session.model, 'lang') =='fr':
        print("[Gladause] Chargement du modèle de langage, veuillez patienter ... \n")
        generate_voice("Chargement du modèle de langage, veuillez patienter ...", VoiceSession('Gladause')) # Gladause = fr version
    elif getattr(voice_session.model, 'lang') =='en':
        print("[Gladaus] Loading language model into memory, please wait ... \n")
        generate_voice("Loading language model into memory, please wait ...") # Default voice -> Gladaus = en version

    # First welcome message of the assistant
    welcome_msg = [{'role': 'system','content': getattr(voice_session.model, 'welcome_prompt')}]
        
    return process_prompt(welcome_msg, llm_model_name, voice_session, False)

# Setup and starts the conversation    
if __name__ == "__main__": 
    try : 
         # Checking if llm is in ollama or try download it
        if(find_or_pull_llm_model(default_llm_model)):
            # Chosing voice model
            print(f'[System] Aviable voice models : {get_voice_names()} \n')
            voice_name = input("Choice (ENTER for default): ")
        
            if not voice_name:
                voice_name = 'Gladaus' # Default Gladaus[en]
            print('')
            start_conversation(voice_name=voice_name, llm_model_name=default_llm_model)
    except Exception as e:
        print(f'[System] ❌ Error : {e}')
