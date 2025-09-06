
# <a href='https://session-bases-chatbot-with-history.streamlit.app'>Conversational Chatbot with History</a>

This project is a **session-based conversational chatbot** built with **Streamlit**, **LangChain**, and **Groq**.  
It allows you to chat with different AI models, manage multiple sessions, and retain conversation history across interactions.

---

## Features
- Multiple session support  
- Conversation history tracking  
- Model, temperature, and token customization  
- Clean Streamlit chat interface  

---

## Setup
1. Clone the repository and enter the project folder:
```bash
   git clone https://github.com/yourusername/chatbot-with-history.git
   cd chatbot-with-history
````

2. Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Groq API key:

   ```ini
   GROQ_API_KEY=your_api_key_here
   ```

---

## Run the App

```bash
streamlit run test.py
```

Open `http://localhost:8501` in your browser to start chatting.

---

## Requirements

* Python 3.9+
* Streamlit
* LangChain
* langchain\_groq
* python-dotenv
