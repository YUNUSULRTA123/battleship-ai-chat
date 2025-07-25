import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from ai import BattleshipAI
from game import Game
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
socketio = SocketIO(app, cors_allowed_origins="*")

# Словари для хранения состояния игры и ИИ по клиентам
games = {}
ai_players = {}

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    # Создаём новую игру и ИИ для подключившегося клиента
    games[request.sid] = Game()
    ai_players[request.sid] = BattleshipAI()
    print(f'Клиент подключился: {request.sid}')
    emit('message', {'user': 'Server', 'msg': 'Добро пожаловать в Морской Бой!'})


@socketio.on('chat_message')
def handle_chat(data):
    print(f"[Чат] {data['user']}: {data['msg']}")
    emit('chat_message', data, broadcast=True)


@socketio.on('player_move')
def handle_player_move(data):
    game = games.get(request.sid)
    ai_player = ai_players.get(request.sid)
    if not game or not ai_player:
        emit('error', {'msg': 'Игра не найдена.'})
        return

    x, y = data['x'], data['y']
    print(f"Игрок {request.sid} стреляет в ({x}, {y})")

    result = game.player_move(x, y)
    emit('move_result', {'x': x, 'y': y, 'result': result})

    if game.is_game_over():
        emit('game_over', {'winner': 'Player'})
        return

    # Ход ИИ
    ai_x, ai_y = ai_player.make_move(game)
    ai_result = game.ai_move(ai_x, ai_y)
    emit('ai_move', {'x': ai_x, 'y': ai_y, 'result': ai_result})

    if game.is_game_over():
        emit('game_over', {'winner': 'AI'})


@socketio.on('disconnect')
def handle_disconnect():
    games.pop(request.sid, None)
    ai_players.pop(request.sid, None)
    print(f'Клиент отключился: {request.sid}')


if __name__ == '__main__':
    socketio.run(app, debug=True)
