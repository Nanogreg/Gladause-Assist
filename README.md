# 🤖 Gladause-Assist

**Gladause-Assist** is a fully local, terminal-based AI assistant. It allows users to interact with an AI via text prompts and receive both text and high-quality voice responses. 

The project leverages **Gemma 4** as the core Large Language Model (LLM) running locally via **Ollama**, and uses **Piper-TTS** for fast and natural offline speech generation.

## 📑 Table of Contents

* [📝 Summary](#-summary)
* [✨ Features](#-features)
* [📂 Project Structure](#-project-structure)
* [🛠️ Prerequisites](#️-prerequisites)
* [🚀 Installation & Setup](#-installation--setup)
* [🎮 Usage](#-usage)
* [🏆 Credits](#-credits)

---

## ✨ Features

* **🧠 100% Local LLM:** Powered by Gemma 4 via local Ollama for complete privacy and offline capabilities.
* **🗣️ Local Text-to-Speech:** Uses Piper-TTS to instantly synthesize the AI's responses into audio.
* **⚡ Fast & Lightweight:** Designed to run efficiently on local hardware.

---

## 📂 Project Structure

    gladause-assist/
    ├── voices/              # Directory containing .onnx and .json voice models
    ├── app.py               # Main application script (Terminal UI & Logic)
    ├── my_piper_tts.py      # Text-to-Speech engine integration
    ├── piper_voice_model.py # Voice data models and configurations
    └── requirements.txt     # Python dependencies

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your system:

1. **Python 3.11**: This project specifically requires Python 3.11.
2. **Ollama**: Required to run the local LLM. 
   * Download and install from [ollama.com](https://ollama.com/).
3. **Gemma 4 Model**: Once Ollama is installed, open your terminal and pull the model by running:
```
ollama run gemma4:e4b
and/or 
ollama run batiai/gemma4-e4b:q4
etc
```
   *(Note: Ensure the Ollama background service is running when using the assistant).*

4. **Linux System - portaudio** : If you are running this project on Linux, you will need to install `portaudio` on your host system to allow the `sounddevice` Python library to playback the generated speech audio:

* **Ubuntu / Debian:**
```
sudo apt-get update
sudo apt-get install libportaudio2
```

* **Fedora / RHEL:**
```
sudo dnf install portaudio
```

---

## 🚀 Installation & Setup

### 1. Set up the Python Virtual Environment
Navigate to the project directory and create a virtual environment specifically using Python 3.11.
We name it `.venv311` in our example:

**On Windows:**

    py -3.11 -m venv .venv311
    .venv311\Scripts\activate

**On Linux / macOS:**

    python3.11 -m venv .venv311
    source .venv311/bin/activate

### 2. Install Dependencies
With the virtual environment activated, install the required Python packages:

    pip install -r requirements.txt

### 3. Setup Voices
🗣️ **Voice Setup Guide:** [voices/voices.md](voices/VOICES.md)

Make sure you have populated the `voices/` directory with your desired Piper-TTS models (both `.onnx` and `.json` files). 
*Please refer to the `VOICES.md` for download links and voice configuration details.*

---

## 🖥️ Usage

1. Ensure your **Ollama server** is running in the background and your voices models are downloaded.
2. Activate your virtual environment (if not already active).
3. Start the assistant by running the main script: app.py
4. Type your prompt in the terminal, press Enter, and wait for the AI to load and reply with text and speech!

---

## 🏆 Credits

This project is made possible thanks to the following incredible open-source projects and models:

* **Piper-TTS**: A fast, local neural text-to-speech engine. 
  * Repository: https://github.com/OHF-Voice/piper1-gpl

* **Gemma 4**: A family of open models built by Google DeepMind. 
  * Read more: https://huggingface.co/google/gemma-4-E4B-it

* **Ollama**: A platform to get up and running with LLMs locally.
  * Official Website: [ollama.com](https://ollama.com/)

* **GLaDOS French Voice**: The custom-trained French GLaDOS voice model created by [TazzerMAN](https://github.com/TazzerMAN/).
  * Repository: https://github.com/TazzerMAN/piper-voice-glados-fr/tree/main