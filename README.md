# battleship-ai-chat

Этот проект реализует онлайн-версию игры "Морской Бой" (Battleship) с использованием Flask, Flask-SocketIO и Eventlet. Игроки могут играть против искусственного интеллекта (AI) через веб-интерфейс. Обмен ходами и сообщениями реализован в реальном времени через WebSocket.

## Особенности

- Реализация классической игры "Морской Бой" против AI.
- Чат для общения между игроком и сервером.
- Ходы игрока и AI обрабатываются в реальном времени.
- Состояние игры и AI отслеживается индивидуально для каждого клиента.
- Поддержка нескольких одновременных игроков.
- Реализация на Flask с асинхронной обработкой через Eventlet.

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/<ваш-репозиторий>/battleship-flask.git
cd battleship-flask
```

### 2. Установите зависимости

Рекомендуется использовать виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**requirements.txt:**
```
Flask
Flask-SocketIO
eventlet
```

### 3. Запустите сервер

```bash
python app.py
```

Сервер будет доступен по адресу: [http://localhost:5000](http://localhost:5000)

### 4. Откройте игру в браузере

Перейдите по адресу [http://localhost:5000](http://localhost:5000) и начните игру!

## Структура проекта

```
├── app.py                # Основной файл приложения Flask
├── ai.py                 # Модуль с реализацией BattleshipAI
├── game.py               # Модуль с логикой игры
├── templates/
│   └── index.html        # Веб-интерфейс игры
├── static/               # Статические файлы (CSS, JS, изображения)
├── requirements.txt      # Список зависимостей
└── README.md             # Данный файл
```

## Основные компоненты

- **app.py**: Запуск Flask-приложения. Обработка WebSocket-событий: `connect`, `chat_message`, `player_move`, `disconnect`.
- **ai.py**: Логика искусственного интеллекта для игры.
- **game.py**: Механика игры, обработка ходов, проверка победы.
- **templates/index.html**: Веб-интерфейс для игры и чата.

## Как работает

- При подключении клиента создаётся новая игра и AI.
- Игрок делает ход — сервер проверяет результат, сообщает о победе, если игра завершена.
- После хода игрока AI делает свой ход.
- Все сообщения чата транслируются всем подключённым клиентам.
- При отключении клиента его состояние игры удаляется с сервера.

## Пример кода: запуск игры

```python
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Ваши обработчики и логика игры

if __name__ == '__main__':
    socketio.run(app, debug=True)
```

## Разработка и доработка

- Для изменения логики AI — редактируйте файл `ai.py`.
- Для изменения правил игры — редактируйте файл `game.py`.
- Для доработки интерфейса — правьте `templates/index.html` и файлы в `static/`.

## Лицензия

Проект распространяется под The Unlicense License лицензией. Используйте свободно!

---

> **Автор:** [Ваше Имя или ник](https://github.com/YUNUSULTRA123)
