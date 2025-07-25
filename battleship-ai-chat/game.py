import random

BOARD_SIZE = 10
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Классическая схема

class Game:
    def __init__(self):
        self.player_board = [['~'] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.ai_board = [['~'] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.ai_hits = [[''] * BOARD_SIZE for _ in range(BOARD_SIZE)]  # Для отображения ходов
        self.place_ships(self.ai_board)
        self.place_ships(self.player_board)  # Можно отключить, если игрок сам расставляет

    def place_ships(self, board):
        for size in SHIP_SIZES:
            placed = False
            while not placed:
                orientation = random.choice(['h', 'v'])
                if orientation == 'h':
                    x = random.randint(0, BOARD_SIZE - size)
                    y = random.randint(0, BOARD_SIZE - 1)
                    if all(board[y][x + i] == '~' for i in range(size)):
                        for i in range(size):
                            board[y][x + i] = 'S'
                        placed = True
                else:
                    x = random.randint(0, BOARD_SIZE - 1)
                    y = random.randint(0, BOARD_SIZE - size)
                    if all(board[y + i][x] == '~' for i in range(size)):
                        for i in range(size):
                            board[y + i][x] = 'S'
                        placed = True

    def player_move(self, x, y):
        if self.ai_board[y][x] in ['X', 'O']:
            return 'repeat'

        if self.ai_board[y][x] == 'S':
            self.ai_board[y][x] = 'X'
            return 'hit'
        else:
            self.ai_board[y][x] = 'O'
            return 'miss'

    def ai_move(self, x, y):
        if self.player_board[y][x] in ['X', 'O']:
            return 'repeat'

        if self.player_board[y][x] == 'S':
            self.player_board[y][x] = 'X'
            self.ai_hits[y][x] = 'X'
            return 'hit'
        else:
            self.player_board[y][x] = 'O'
            self.ai_hits[y][x] = 'O'
            return 'miss'

    def is_game_over(self):
        # Проверяем, остались ли у кого-то корабли
        def has_ships(board):
            return any(cell == 'S' for row in board for cell in row)

        player_alive = has_ships(self.player_board)
        ai_alive = has_ships(self.ai_board)
        return not (player_alive and ai_alive)

#Пояснения:
#'~' — пустая клетка
#'O' — промах
#'S' — корабль
#'X' — попадание