3
import random
import math
import os
import time

# ------------------ Board ------------------
class Board:
    def __init__(self, size=3):
        self.size = size
        self.grid = [[str(i * size + j + 1) for j in range(size)] for i in range(size)]

    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nBoard\n-----")

        for r in range(self.size):
            print(" | ".join(self.grid[r]))

            if r < self.size - 1:
                print("-" * (self.size * 4 - 3))

        print()

    def available_moves(self):
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.grid[r][c].isdigit()
        ]

    def make_move(self, r, c, symbol):
        if self.grid[r][c].isdigit():
            self.grid[r][c] = symbol
            return True

        return False

    def check_winner(self):
        lines = []

        # Rows and columns
        for i in range(self.size):
            lines.append(self.grid[i])
            lines.append([self.grid[r][i] for r in range(self.size)])

        # Diagonals
        lines.append([self.grid[i][i] for i in range(self.size)])
        lines.append([
            self.grid[i][self.size - i - 1]
            for i in range(self.size)
        ])

        # Check winner
        for line in lines:
            if all(cell == "X" for cell in line):
                return "X"

            if all(cell == "O" for cell in line):
                return "O"

        # Check tie
        if not self.available_moves():
            return "Tie"

        return None


# ------------------ Player ------------------
class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, board: Board):
        raise NotImplementedError


# ------------------ Human Player ------------------
class HumanPlayer(Player):
    def make_move(self, board: Board):

        while True:
            try:
                move = int(
                    input(f"نوبت {self.symbol} (1-{board.size**2}): ")
                )

                # Check input range
                if move < 1 or move > board.size**2:
                    print("شماره خانه نامعتبر است، دوباره تلاش کن.")
                    continue

                move -= 1

                r, c = divmod(move, board.size)

                if board.make_move(r, c, self.symbol):
                    break
                else:
                    print("خانه پر شده، دوباره امتحان کن.")

            except ValueError:
                print("ورودی نامعتبر، دوباره تلاش کن.")


# ------------------ AI Base ------------------
class AIPlayer(Player):
    def __init__(self, symbol, level='easy'):
        super().__init__(symbol)
        self.level = level

    def make_move(self, board: Board):

        print(
            f"\nهوش مصنوعی ({self.level}) در حال فکر کردن است..."
        )

        time.sleep(0.7)

        if self.level == 'easy':
            EasyAI(self.symbol).make_move(board)

        elif self.level == 'medium':
            MediumAI(self.symbol).make_move(board)

        else:
            HardAI(self.symbol).make_move(board)


# ------------------ Easy AI ------------------
class EasyAI(AIPlayer):
    def make_move(self, board: Board):

        move = random.choice(board.available_moves())

        board.make_move(
            move[0],
            move[1],
            self.symbol
        )

        print(
            f"هوش مصنوعی ({self.symbol}) حرکت تصادفی انجام داد."
        )


# ------------------ Medium AI ------------------
class MediumAI(AIPlayer):
    def make_move(self, board: Board):

        opponent = "O" if self.symbol == "X" else "X"

        # Check winning move
        for (r, c) in board.available_moves():

            board.grid[r][c] = self.symbol

            if board.check_winner() == self.symbol:
                print(
                    f"هوش مصنوعی ({self.symbol}) حرکت برنده انجام داد."
                )
                return

            board.grid[r][c] = str(
                r * board.size + c + 1
            )

        # Check defensive move
        for (r, c) in board.available_moves():

            board.grid[r][c] = opponent

            if board.check_winner() == opponent:

                board.grid[r][c] = self.symbol

                print(
                    f"هوش مصنوعی ({self.symbol}) حرکت دفاعی انجام داد."
                )

                return

            board.grid[r][c] = str(
                r * board.size + c + 1
            )

        # Random move
        EasyAI(self.symbol).make_move(board)


# ------------------ Hard AI ------------------
class HardAI(AIPlayer):

    def minimax(self, board: Board, depth, is_maximizing):

        result = board.check_winner()

        opponent = "O" if self.symbol == "X" else "X"

        # AI wins
        if result == self.symbol:
            return 10 - depth

        # Opponent wins
        elif result == opponent:
            return depth - 10

        # Tie
        elif result == "Tie":
            return 0

        # Maximizing
        if is_maximizing:

            best_val = -math.inf

            for (r, c) in board.available_moves():

                board.grid[r][c] = self.symbol

                val = self.minimax(
                    board,
                    depth + 1,
                    False
                )

                board.grid[r][c] = str(
                    r * board.size + c + 1
                )

                best_val = max(best_val, val)

            return best_val

        # Minimizing
        else:

            best_val = math.inf

            for (r, c) in board.available_moves():

                board.grid[r][c] = opponent

                val = self.minimax(
                    board,
                    depth + 1,
                    True
                )

                board.grid[r][c] = str(
                    r * board.size + c + 1
                )

                best_val = min(best_val, val)

            return best_val

    def make_move(self, board: Board):

        best_val = -math.inf
        best_move = None

        for (r, c) in board.available_moves():

            board.grid[r][c] = self.symbol

            val = self.minimax(
                board,
                0,
                False
            )

            board.grid[r][c] = str(
                r * board.size + c + 1
            )

            if val > best_val:
                best_val = val
                best_move = (r, c)

        if best_move:

            board.make_move(
                best_move[0],
                best_move[1],
                self.symbol
            )

            print(
                f"هوش مصنوعی ({self.symbol}) بهترین حرکت را انتخاب کرد."
            )


# ------------------ Game ------------------
class Game:

    def __init__(
        self,
        size=3,
        mode='1',
        difficulty='easy'
    ):

        self.board = Board(size)

        self.mode = mode
        self.difficulty = difficulty

        self.turn = "X"

        self.create_players()

    def create_players(self):

        if self.mode == '2':

            self.player1 = HumanPlayer("X")
            self.player2 = HumanPlayer("O")

        else:

            self.player1 = HumanPlayer("X")
            self.player2 = AIPlayer(
                "O",
                self.difficulty
            )

    def switch_turn(self):

        self.turn = "O" if self.turn == "X" else "X"

    def get_current_player(self):

        if self.turn == "X":
            return self.player1

        return self.player2

    def play(self):

        while True:

            self.board.display()

            winner = self.board.check_winner()

            if winner:

                self.board.display()

                if winner == "Tie":
                    print("بازی مساوی شد!")

                else:
                    print(f"برنده: {winner}")

                break

            current_player = self.get_current_player()

            current_player.make_move(self.board)

            self.switch_turn()


# ------------------ Start Game ------------------
if __name__ == "__main__":

    print("=== 🎮 بازی شیءگرای XO با سه سطح سختی ===")

    # Board size
    while True:

        try:
            size = int(input("اندازه بورد (مثلاً 3): "))

            if size < 3:
                print("اندازه بورد باید حداقل 3 باشد.")
                continue

            break

        except ValueError:
            print("لطفاً یک عدد وارد کن.")

    # Game mode
    while True:

        mode = input(
            "حالت بازی: 1) انسان vs AI  2) انسان vs انسان → "
        )

        if mode in ['1', '2']:
            break

        print("لطفاً فقط 1 یا 2 را وارد کن.")

    # Difficulty
    difficulty = "easy"

    if mode == "1":

        while True:

            difficulty = input(
                "سطح سختی (easy / medium / hard): "
            ).lower()

            if difficulty in ['easy', 'medium', 'hard']:
                break

            print(
                "سطح سختی نامعتبر است. "
                "یکی از easy / medium / hard را وارد کن."
            )

    # Create and start game
    game = Game(
        size,
        mode,
        difficulty
    )

    game.play()


