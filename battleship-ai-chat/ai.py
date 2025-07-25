import random

BOARD_SIZE = 10

class BattleshipAI:
    def __init__(self):
        # Все возможные ходы
        self.available_moves = [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE)]
        random.shuffle(self.available_moves)

    def make_move(self, game):
        while self.available_moves:
            x, y = self.available_moves.pop()
            # Если поле пустое (не помечено X или O), возвращаем ход
            if game.player_board[y][x] not in ('X', 'O'):
                return (x, y)
        # Если ходов нет, возвращаем None или фиктивный ход
        return None

# Пример заглушки игрового поля
class Game:
    def __init__(self):
        # Пустая доска
        self.player_board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def apply_move(self, x, y, mark='O'):
        # Отмечаем ход на доске
        self.player_board[y][x] = mark

# Тестирование ИИ
game = Game()
ai = BattleshipAI()

for _ in range(5):  # сделаем 5 ходов ИИ
    move = ai.make_move(game)
    if move is None:
        print("Ходы закончились")
        break
    x, y = move
    print(f"ИИ делает ход: {x}, {y}")
    game.apply_move(x, y, 'O')
