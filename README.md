# Simple Telegram Bot

Простой учебный Telegram-бот на Python.

## Возможности

* Обработка стандартных команд:

    * `/start` — приветственное сообщение
    * `/help` — справка по доступным командам
    * `/about` — информация о боте и авторе
* Загрузка конфигурации из `.env` файла
* Логирование в файл и консоль с настройкой уровня логов

---

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ArsKF/tg-bot-simple.git
cd telegram-bot-simple
```

### 2. Установить зависимости

Рекомендуется использовать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

Установить пакеты:

```bash
pip install -r requirements.txt
```

### 3. Настроить переменные окружения

Скопировать пример файла:

```bash
cp .env.example .env
```

Отредактировать `.env`, указав данные:

```env
TOKEN="токен_от_BotFather"
LOG_FILE="./bot.log"
LOG_LEVEL="INFO"
```

### 4. Запустить бота

```bash
python main.py
```

---

## Логирование

Все действия бота логируются:

* в файл (путь задаётся через `LOG_FILE`)
* в консоль

Формат:

```
2025-09-18 12:34:56 - telegram-bot - INFO - Telegram Bot started.
```

---

## 👤 Автор

Агаев Арсений Валерьевич
ID: 1032221668
