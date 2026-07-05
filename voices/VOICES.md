# 🎙️ Piper Voices Configuration

To use these voices with the assistant, you must download **both** the `.onnx` model file and its corresponding `.json` configuration file.

---

## 📦 Default Voices

The project is pre-configured to look for and support the following French voice models:

* **GLaDOS:** `fr_FR-glados-medium.onnx`
* **Siwis:** `fr_FR-siwis-medium.onnx`
* **Tom:** `fr_FR-tom-medium.onnx`
* **UPMC:** `fr_FR-upmc-medium.onnx`

---

## 📂 Installation Directory

Place all downloaded files inside the `voices/` directory at the root of your project:

```text
gladause-assist/
├── voices/
│   ├── fr_FR-glados-medium.onnx
│   ├── fr_FR-glados-medium.onnx.json
│   └── [other_voices]...
└── gladause_app.py
```

---

## 📥 Download Links

### 1. Default Official Voices
A wide variety of official multi-language models (high, medium, and low quality).
* **URL:** https://huggingface.co/rhasspy/piper-voices/tree/main

### 2. GLadause (GlaDOS) French Voice (Custom)
The custom-trained French GLaDOS voice model for the Gladause project.
* **URL:** https://github.com/TazzerMAN/piper-voice-glados-fr/tree/main



> 💡 Make sure the `.onnx` and `.json` files have the exact same base name (e.g., `voice.onnx` and `voice.onnx.json`) so that the Piper engine can automatically pair them together.