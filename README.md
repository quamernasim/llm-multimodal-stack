# Assistant

This project sets up services required for running an AI assistant in containerized way.

## 🚀 Features

- **Uses `uv` for package management** (faster than `pip`)
- **Containerized services** to avoid excessive host pollution

---

## 📦 Installation

### **Install docker and uv**

### **Clone the Repository**

```sh
git clone https://github.com/NarendraPatwardhan/Assistant.git
cd Assistant
```

curl -LsSf https://astral.sh/uv/install.sh | sh

sudo apt-get update

sudo dpkg -i --force-overwrite /var/cache/apt/archives/python3.12_3.12.10-1+focal1_amd64.deb
sudo dpkg -i --force-overwrite /var/cache/apt/archives/libpython3.12-stdlib_3.12.10-1+focal1_amd64.deb
sudo apt-get install -f
sudo apt-get upgrade


sudo apt-get install portaudio19-dev

http://5.178.113.239:8000/docs

---

## 🔧 Usage

### **Step 1: Set Up a Virtual Environment**

```sh
uv sync --frozen --no-cache
```

### **Step 2: Build and run docker services**

Run the following commands

```sh
docker compose build [-e WITH_CUDA]
docker compose build --build-arg WITH_CUDA=1
docker compose up -d
docker compose down -v
```

### **Step 3: Run the main script**

```sh
uv run main.py
```

---

## 🔧 Development

### **Development of Individual Modules is described within their READMEs**

## **Notebooks for System Checks**

```sh
uv run --with jupyter jupyter lab
```

---

## 🛠️ How It Works

1. Individual services **download the model they need automatically**
2. **Records audio as `.wav` file**
3. **Runs Whisper inference**
4. **Uses Llama to convert transcription to intent using grammar and system prompt**
5. **Uses Llama to convert request, intent pair into assistant response**
6. **Runs KokoroTTS to return audio**

---

## 🏗️ Project Structure

```
Assistant/
│── compose.yml       # For operationalizing
│── README.md         # Project documentation
│── main.py           # FastAPI server with async transcription
│── .venv/            # Virtual environment (if sync is ran)
```

---

## Potential Improvements

- [ ] Table gen for intent
- [ ] Shift to better model Llama3.1 8B/Qwen/Mistral for Intent & Response
- [ ] Shift to Orpheus-TTS (after Italian/Multilingual release or finetune)

---

## 📬 Contact

For issues or contributions, open a GitHub issue or contact [narendra@machinelearning.one].
