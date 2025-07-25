const BOARD_SIZE = 10;

const socket = io();

const playerBoard = document.getElementById('player-board');
const aiBoard = document.getElementById('ai-board');
const statusEl = document.getElementById('status');
const chatBox = document.getElementById('chat-box');
const chatInput = document.getElementById('chat-input');

let playerTurn = true;  // Кто ходит

// Создаём игровое поле (10x10) для указанного контейнера
function createBoard(container, clickable = false) {
  container.innerHTML = '';
  for (let y = 0; y < BOARD_SIZE; y++) {
    for (let x = 0; x < BOARD_SIZE; x++) {
      const cell = document.createElement('div');
      cell.classList.add('cell');
      cell.dataset.x = x;
      cell.dataset.y = y;
      if (clickable) {
        cell.addEventListener('click', () => {
          if (!playerTurn) {
            alert('Сейчас ход ИИ, подожди!');
            return;
          }
          if (cell.classList.contains('hit') || cell.classList.contains('miss')) {
            alert('Уже стрелял сюда!');
            return;
          }
          makeMove(x, y);
        });
      }
      container.appendChild(cell);
    }
  }
}

// Отправка хода игрока на сервер
function makeMove(x, y) {
  socket.emit('player_move', { x, y });
  playerTurn = false;
  statusEl.textContent = 'Ждём ход ИИ...';
}

// Обработка результата хода игрока
socket.on('move_result', (data) => {
  const { x, y, result } = data;
  const cell = aiBoard.querySelector(`[data-x="${x}"][data-y="${y}"]`);
  if (!cell) return;

  if (result === 'hit') {
    cell.classList.add('hit');
  } else if (result === 'miss') {
    cell.classList.add('miss');
  } else if (result === 'repeat') {
    alert('Вы уже стреляли в эту клетку!');
  }
});

// Обработка хода ИИ
socket.on('ai_move', (data) => {
  const { x, y, result } = data;
  const cell = playerBoard.querySelector(`[data-x="${x}"][data-y="${y}"]`);
  if (!cell) return;

  if (result === 'hit') {
    cell.classList.add('hit');
  } else if (result === 'miss') {
    cell.classList.add('miss');
  }
  playerTurn = true;
  statusEl.textContent = 'Ваш ход!';
});

// Обработка окончания игры
socket.on('game_over', (data) => {
  if (data.winner === 'Player') {
    alert('Поздравляем! Вы выиграли!');
  } else {
    alert('ИИ победил. Попробуйте ещё раз!');
  }
  statusEl.textContent = 'Игра окончена';
  playerTurn = false;
});

// Чат — получение сообщений
socket.on('chat_message', (data) => {
  const msgEl = document.createElement('p');
  msgEl.textContent = `${data.user}: ${data.msg}`;
  chatBox.appendChild(msgEl);
  chatBox.scrollTop = chatBox.scrollHeight;
});

// Чат — отправка сообщений
function sendMessage() {
  const msg = chatInput.value.trim();
  if (msg === '') return;
  socket.emit('chat_message', { user: 'Игрок', msg });
  chatInput.value = '';
}

// Инициализация полей
createBoard(playerBoard, false);  // Твоё поле — просто отображение (потом можно добавить расстановку)
createBoard(aiBoard, true);       // Поле ИИ — кликабельно для стрельбы

statusEl.textContent = 'Ваш ход!';

// Чтобы отправить сообщение по Enter
chatInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});
