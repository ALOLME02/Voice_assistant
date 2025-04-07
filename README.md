# Voice_assistant

## Инструкция по запуску голосового ассистента на Ubuntu 22.04

### 1. Установка необходимых зависимостей

Откройте терминал и выполните следующие команды:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv portaudio19-dev espeak-ng ffmpeg -y
```

Создайте виртуальное окружение и активируйте его:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Установка библиотек Python

Установите все необходимые Python-пакеты:

```bash
pip install numpy sounddevice faster-whisper ollama
```

### 3. Установка и запуск Ollama

Установите Ollama, следуя официальной документации:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Запустите сервер Ollama:

```bash
ollama serve
```

Загрузите модель Qwen2.5-coder:

```bash
ollama pull qwen2.5-coder
```

### 4. Запуск скрипта

Создайте файл с кодом, например, `main.py`, затем запустите его:

```bash
python maint.py
```


