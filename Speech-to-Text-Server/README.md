# Speech-To-Text Server

This project sets up an **asynchronous FastAPI server** for transcribing `.wav` audio files using OpenAI's Whisper model from Hugging Face Transformers.

## 🚀 Features
- **FastAPI-based** server for handling transcription requests
- **Fully asynchronous** using `asyncio` to prevent blocking
- **Supports only `.wav` files** for simplicity
- **Uses `uv` for package management** (faster than `pip`)

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
  'http://localhost:8000/transcribe/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_audio.wav'
```
Or use FastAPI’s built-in interactive UI at:
```
http://localhost:8000/docs
```

---

## 📜 API Endpoints
### **POST /transcribe/**
- **Description:** Accepts `.wav` files and returns the transcribed text.
- **Request Body:**
  - `file`: The `.wav` audio file.
- **Response:**
```json
{
  "transcription": "Transcribed text here"
}
```

---

## 🛠️ How It Works
1. **Loads Whisper model** from Hugging Face (`openai/whisper-tiny`)
2. **Accepts `.wav` file uploads**
3. **Reads audio file asynchronously**
4. **Runs Whisper inference in a separate thread** using `asyncio.to_thread()`
5. **Returns transcription as JSON**

---

## 🏗️ Project Structure
```
Speech-to-Text-Server/
.
├── archive/                ← Archived legacy files
│   ├── main_new_old.py
│   └── main_old.py
├── config/                 ← Central configuration (e.g., constants, env settings)
│   └── constants.py
├── core/                   ← Core business logic
│   ├── model.py            ← Whisper model loading/inference
│   ├── preprocessing.py    ← Audio preprocessing (resampling, mono, etc.)
│   └── transcriber.py      ← ASR pipeline and orchestration
├── Dockerfile              ← Containerized deployment
├── main.py                 ← FastAPI app entrypoint
├── pyproject.toml          ← Dependencies and metadata (Poetry or PEP 621-based)
├── README.md               ← Project documentation
└── uv.lock                 ← Lock file for reproducible builds

```



---

## ⚡ Performance Optimization
- **Inference runs in a separate thread** to avoid blocking FastAPI’s event loop
- **Uses `uv` for faster package management**
- **Preloads Whisper model** to reduce startup time

---

## 📬 Contact
For issues or contributions, open a GitHub issue or contact [narendra@machinelearning.one].
