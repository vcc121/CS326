# game.py

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X = AI (MAX), O = opponent

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def get_actions(self):
        actions = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    actions.append((i, j))
        return actions

    def apply_move(self, action):
        i, j = action
        if self.board[i][j] != ' ':
            raise Exception("Invalid move")

        self.board[i][j] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def copy(self):
        new_game = TicTacToe()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        return new_game

    def result(self, action):
        new_state = self.copy()
        new_state.apply_move(action)
        return new_state

    def check_winner(self):
        lines = []

        # Rows and Columns
        for i in range(3):
            lines.append(self.board[i])  # row
            lines.append([self.board[0][i], self.board[1][i], self.board[2][i]])  # col

        # Diagonals
        lines.append([self.board[0][0], self.board[1][1], self.board[2][2]])
        lines.append([self.board[0][2], self.board[1][1], self.board[2][0]])

        for line in lines:
            if line[0] != ' ' and line[0] == line[1] == line[2]:
                return line[0]

        return None

    def is_terminal(self):
        if self.check_winner() is not None:
            return True
        if len(self.get_actions()) == 0:
            return True
        return False

    def utility(self):
        winner = self.check_winner()

        if winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        else:
            return 0