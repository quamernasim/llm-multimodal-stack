# Text-to-Speech Server

This project sets up an asynchronous FastAPI server for generating .wav audio files from text using KokoroTTS Italia.

## 🚀 Features
- **FastAPI-based** server for handling TTS requests
- **Fully asynchronous** using asyncio to prevent blocking
- **Returns .wav audio files** directly as a response
- **Uses `uv` for package management** (faster than pip)

---

## 🔧 Usage
### **Step 1: Set Up a Virtual Environment**
```sh
uv sync --frozen --no-cache
```

### **Step 2: Start the Server**
Run the following command to start the FastAPI server:
```sh
uv run main.py
```

### **Alternatively: Using Docker**
```sh
docker build -t {name} .
```


```sh
docker run -p {port}:8000 {name}
```

### **Test the API**
You can test using `curl`:
```sh
curl -X 'POST' \
  'http://localhost:8000/synthesize/' \
  -H 'accept: audio/wav' \
  -H 'Content-Type: application/json' \
  -d '{"text": "Come stai?"}' \
  --output output.wav
```
Or use FastAPI’s built-in interactive UI at:
```
http://localhost:8000/docs
```

---

## 📜 API Endpoints
### **POST /synthesize/**
- **Description:** Accepts text input and returns a .wav file.
- **Request Body:**
  - `text`: The text to convert to speech.
- **Response**:
  Returns a `.wav` audio file as a binary response.

---

## 🛠️ How It Works
1. **Loads KokoroTTS model** with Italian configuration
2. **Processes input text asynchronously**
3. **Returns the generated .wav file directly** in the response

---

## 🏗️ Project Structure
```
Text-to-Speech-Server/
│── Dockerfile        # For operationalizing 
│── README.md         # Project documentation
│── main.py           # FastAPI server with async synthesizing
│── .venv/            # Virtual environment (if sync is ran)
```

---

## ⚡ Performance Optimization
- **Inference runs in a separate thread** to avoid blocking FastAPI’s event loop
- **Uses `uv` for faster package management**
- **Preloads SpeechT5 model** to reduce startup time

---

## 📬 Contact
For issues or contributions, open a GitHub issue or contact [quamer23nasim38@gmail.com].
