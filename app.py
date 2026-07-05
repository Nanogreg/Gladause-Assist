import ollama
from my_piper_tts import generate_voice
from piper_voice_model import get_voice_by_name, get_voice_names

# Model list
gemma4_e4b = 'gemma4:e4b'               # Full e4b model
gemma4_e4b_q4 = 'batiai/gemma4-e4b:q4'  # e4b quantized Q4
gemma4_e4b_q6 = 'batiai/gemma4-e4b:q6'  # e4b quantized Q6
gemma4_uncensored = """
mdhm_hmmd/gemma4-e4b-uncensored-q8"""   # e4b uncensored quantized Q8
gemma4_9b = 'gemma2:9b'
llm_model_name: str                     # Used model

def start_conversation(voice_model: str = 'Gladause', stream_conv: bool = True):
    """Starts a conversation between the user and the AI with text + speach response using Gemma4 and Piper-tts.

    Args:
        stream_conv (bool, optional): Specify if the text and voice are generated in one block or streamed. Defaults to True.
        voice_model (str, optional): Voice model name to use (see: piper_voice_model.py). Defaults to 'Gladause'.
    """
    
    #Model preload --> !!! to fix
    #ollama.pull(model_name)
    #ollama.chat(model=model_name, keep_alive="10m")
    
    # Getting the voice model
    voice = get_voice_by_name(voice_model)
    if not voice:
        print(f"Error getting the voice : {voice_model}\n=== Exit ===")
        generate_voice("Erreur de chargement de la configuration.", voice_name='Gladause')
        return
    
    # Welcome msg
    print(f"[{voice.name}] Bonjour, comment puis-je t'aider ?")
    generate_voice("Bonjour : comment puis-je t'aider ?", voice_name=voice.name)

    # First conversaion history with system role
    messages = [{'role': 'system','content': "Tu es une assistante cynique appellée Gladause. Tu réponds sans emoji ou caractères spéciaux en quelques phrases. Tu réponds aux questions avec cynisme et n'hésite pas à engager la conversation sur d'autres sujets de manière désabusée. Ta voix est basée sur celle de Glados, une IA présente dans l'univers de Portal, mais tu es bien Gladause, pas Glados."}]

    # First prompt out of the loop to handle quit at 1st msg
    user_prompt = input('\n[Moi] ').strip()

    while True:
        user_prompt = user_prompt.strip()

        if user_prompt.strip().lower() in ['exit', 'quit', 'end', 'quitter', 'fin']:
            break
        
        # Adding user prompt to the conv history
        messages.append({
            'role': 'user', 
            'content': user_prompt
        })
        
        # Getting text response
        response_data  = ollama.chat(
            model=llm_model_name,
            messages=messages,
            think=False,
            stream=stream_conv,
            options={
                'num_ctx': 1024,    # Reduces memory overhead significantly
                'num_predict': 256, # Limits maximum length of the response
                'num_thread': 8,    # CPU cores
                'num_gpu' : 99      # Offload to gpu
            },
        )

        print(f'\n[{voice.name}] ', end='')

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
                    generate_voice(response_part, voice_name=voice.name)
                    response_part = ''
            print('')
        else:
            assistant_response = response_data['message']['content'] # type: ignore
            print(assistant_response)
            generate_voice(assistant_response, voice_name=voice.name) 

        # Adding assistant response to the conv history
        messages.append({
            'role': 'assistant',
            'content': assistant_response
        })
        
        user_prompt = input('\n[Moi] ').strip()
   
# Setup and starts the conversation    
if __name__ == "__main__": 
    llm_model_name = gemma4_e4b_q4
    
    print(f'=== Aviable models : {get_voice_names()} ===\n')
    voice_model = input("Choice (ENTER for default): ")
    if not voice_model:
        voice_model = 'Gladause'
    print('')
    start_conversation(voice_model=voice_model)
