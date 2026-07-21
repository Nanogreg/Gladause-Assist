import ollama
from my_piper_tts import generate_voice

class GemmaModels():
    gemma4_e4b = 'gemma4:e4b' #9.6gb
    gemma4_e4b_q4 = 'batiai/gemma4-e4b:q4' #5.3gb
    gemma4_e2b_q4 = 'batiai/gemma4-e2b:q4' #3.4gb
    gemma4_e4b_q6 = 'batiai/gemma4-e4b:q6'
    gemma4_e4b_uncensored = 'mdhm_hmmd/gemma4-e4b-uncensored-q8:latest' #8.1gb

def find_or_pull_llm_model(llm_model: str)-> bool:
    """Check If the LLM model name is aviable in ollama and try downloading it if it's missing. 
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
        