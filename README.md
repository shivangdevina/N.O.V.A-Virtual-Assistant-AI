# N.O.V.A AI Assistant

**N.O.V.A AI Assistant** is a **Python-based desktop application** that provides an interactive, voice-activated AI assistant with a sleek **PyQt5 GUI**.

It supports voice commands, real-time web searches, automation tasks, text-to-speech, speech-to-text, and image generation. The application leverages multiple APIs and libraries, including **Groq** for conversational AI, **Cohere** for decision-making, and **Hugging Face** for image generation.

---

## 🚀 Features

- **Voice Interaction:** Supports speech-to-text input and text-to-speech responses using Selenium and edge-tts.
- **Conversational AI:** Powered by Groq's LLaMA model for general and real-time queries.
- **Automation:** Opens/closes applications, plays YouTube videos, controls system tasks (e.g., mute, volume), and performs Google/YouTube searches.
- **Image Generation:** Generates images based on user prompts using Hugging Face's Stable Diffusion.
- **Real-Time Search:** Fetches up-to-date information via Google Search integration.
- **GUI:** Responsive PyQt5 interface with customizable top bar, chat section, and animated GIFs.
- **Multilingual Support:** Translates non-English input to English using `mtranslate`.
- **Persistent Chat History:** Stores conversations in `Data/ChatLog.json`.

---

## 🛠️ Tech Stack

### Backend
- **Python 3.x**
- **Groq (LLaMA3-70B)** for conversational AI
- **Cohere** for decision-making model
- **Hugging Face** (Stable Diffusion) for image generation
- **edge-tts** for text-to-speech
- **Selenium** with WebDriver Manager for speech-to-text
- **pywhatkit**, **AppOpener**, **keyboard** for automation
- **Requests**, **BeautifulSoup**, **googlesearch-python** for web scraping/search

### Frontend
- **PyQt5** for GUI
- Custom CSS-like styling with GIF animations

### Storage
- **JSON** for chat history (`Data/ChatLog.json`)
- File-based storage for temp data and generated images

### Environment
- **python-dotenv** for configuration management

---

## ✅ Prerequisites

Before you begin, make sure you have:

- **Python 3.8 or higher**
- **pip** for installing dependencies
- **Google Chrome** (for Selenium-based speech recognition)
- Accounts and API keys for:
  - **Groq** (conversational AI)
  - **Cohere** (decision-making)
  - **Hugging Face** (image generation)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd N.O.V.A-ai-assistant
