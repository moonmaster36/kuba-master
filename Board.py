import copy


class Player:
    def __init__(self, name, marble_color):
        self.name = name
        self.marble_color = marble_color
        self.marble_count = 8
        self.captured_count = 0

    def get_name(self):
        return self.name

    def get_marble_color(self):
        return self.marble_color

    def get_marble_count(self):
        return self.marble_count

    def get_captured_count(self):
        return self.captured_count

    def set_marble_count(self, x):
        self.marble_count = x

    def decrement_marble_count(self, x):
        self.marble_count -= x

    def increase_captured_count(self, x):
        self.captured_count += x


class Kuba:
    ROW_RANGE = 7
    COL_RANGE = 7

    def __init__(self, p1: tuple, p2: tuple):
        self.p1 = Player(p1[0], p1[1])
        self.p2 = Player(p2[0], p2[1])
        self.board = [[' ' for _ in range(self.ROW_RANGE)] for _ in range(self.COL_RANGE)]
        self.red_marbles = 13
        self.white_marbles = 8
        self.black_marbles = 8
        self.current_turn = None
        self.winner = None

    def set_turn(self, x):
        self.current_turn = x

    def get_board(self):
        return self.board

    def get_current_turn(self):
        return self.current_turn

    def get_winner(self):
        if self.winner:
            return self.winner.get_name()
        else:
            return None

    def get_captured(self, playername):
        if self.p1.get_name() == playername:
            return self.p1.get_captured_count()
        else:
            return self.p2.get_captured_count()

    def get_marble(self, coords: tuple):
        """Return the marble at the given position"""
        row = coords[0]
        col = coords[1]
        # Determine if coords are valid
        if 0 <= row < self.ROW_RANGE and 0 <= col < self.COL_RANGE:
            return self.board[row][col]

    def get_marble_count(self):
        white, black, red = 0, 0, 0

        for i in range(self.COL_RANGE):
            for j in range(self.ROW_RANGE):
                current_marble = self.board[i][j]
                if current_marble == 'W':
                    white += 1
                elif current_marble == 'B':
                    black += 1
                elif current_marble == 'R':
                    red += 1
        return white, black, red

    def showBoard(self):
        for i in range(self.COL_RANGE):
            print(self.board[i])
        print()

    def clearBoard(self):
        for i in range(self.COL_RANGE):
            self.board[i].clear()
        self.board = [[' ' for _ in range(self.ROW_RANGE)] for _ in range(self.COL_RANGE)]

    def showGame(self):
        """Prints various details about the game."""
        print(F'-------- Game Details --------')
        print(f'Board Status: \nWhite: {self.white_marbles} \nBlack: {self.black_marbles} \nRed: {self.red_marbles}')
        print(f'Winner: {self.get_winner()}')
        print(f'Turn: {self.get_current_turn()}')

        print()
        print(F'Player 1: {self.p1.get_name()}')
        print(F'Marble Color: {self.p1.get_marble_color()}')
        print(f'Marble Count: {self.p1.get_marble_count()}')
        print(F'Captured: {self.get_captured(self.p1.get_name())}')
        print()
        print(F'Player 2: {self.p2.get_name()}')
        print(F'Marble Color: {self.p2.get_marble_color()}')
        print(f'Marble Count: {self.p2.get_marble_count()}')
        print(F'Captured: {self.get_captured(self.p2.get_name())}')
        print('------------------------------')

    def setupBoard(self):
        # Top left
        self.board[0][0] = 'W'
        self.board[0][1] = 'W'
        self.board[1][0] = 'W'
        self.board[1][1] = 'W'

        # Top right
        self.board[0][6] = 'B'
        self.board[0][5] = 'B'
        self.board[1][5] = 'B'
        self.board[1][6] = 'B'

        # Bottom Left
        self.board[5][0] = 'B'
        self.board[5][1] = 'B'
        self.board[6][0] = 'B'
        self.board[6][1] = 'B'

        # Bottom Right
        self.board[5][5] = 'W'
        self.board[5][6] = 'W'
        self.board[6][5] = 'W'
        self.board[6][6] = 'W'

        # Red marbles
        self.board[1][3] = 'R'
        self.board[2][2] = 'R'
        self.board[2][3] = 'R'
        self.board[2][4] = 'R'
        self.board[3][1] = 'R'
        self.board[3][2] = 'R'
        self.board[3][3] = 'R'
        self.board[3][4] = 'R'
        self.board[3][5] = 'R'
        self.board[4][2] = 'R'
        self.board[4][3] = 'R'
        self.board[4][4] = 'R'
        self.board[5][3] = 'R'

    def get_player(self, playername):
        """Returns the player object given a player name."""
        if self.p1.get_name() == playername:
            return self.p1

        if self.p2.get_name() == playername:
            return self.p2

    def get_opposite_marble(self, coords: tuple, direction: str):
        """
        Return marble in space opposite of direction. If no marble in space opposite,
        returns None.
        """
        row = coords[0]
        col = coords[1]
        candidate_coords = None
        # Check if marble exists in opposite location of direction of move.
        # Check forward space.
        if direction == 'B':
            candidate_coords = (row - 1, col)  # Check forward space.
        # Check
        if direction == 'R':
            candidate_coords = (row, col - 1)  # Check left space.

        if direction == 'F':
            candidate_coords = (row + 1, col)  # Check backward space.

        if direction == 'L':
            candidate_coords = (row, col + 1)  # Check right space
        opposite_marble = self.get_marble(candidate_coords)
        return opposite_marble

    def validate_move(self, playername: str, coords: tuple, direction: str) -> bool:
        """Validates a move"""
        # Verify that the player is allowed to move the chosen marble.
        candidate_marble = self.get_marble(coords)
        candidate_player = self.get_player(playername)

        if candidate_marble != candidate_player.get_marble_color():
            return False

        # Move has been made and it is not playername's turn
        if self.get_current_turn() and self.get_current_turn() != playername:
            return False

        # Check for space to push.
        opposite_marble = self.get_opposite_marble(coords, direction)

        # Pushing from edge
        if opposite_marble == 'W' or opposite_marble == 'B' or opposite_marble == 'R':
            return False

        # Check if move will push player's own marble off

        return True

    def make_move(self, playername: str, coords: tuple, direction: str) -> bool:
        # print(F'{playername} attempting to move {coords} {direction}')
        # print(F'marble @ {coords} = {self.get_marble(coords)}')
        valid = self.validate_move(playername, coords, direction)
        if not valid:
            return False

        current_player = self.get_player(playername)

        # Get move range
        # RIGHT MOVEMENT ONLY
        if direction == 'R':
            row = coords[0]
            col = coords[1]
            start = coords[1]
            cur_row = self.board[row]
            successful_right_move = self.move_right(self.board[row], start)

            if not successful_right_move:
                return False

        # Assuming move was valid, so switch current turn for next current_turn
        if self.p1.get_name() == playername:
            self.current_turn = self.p2.get_name()
        else:
            self.current_turn = self.p1.get_name()

        # Update all marble counts
        new_counts = self.get_marble_count()
        self.white_marbles = new_counts[0]
        self.black_marbles = new_counts[1]
        self.red_marbles = new_counts[2]

        if self.p1.get_marble_color() == 'W':
            self.p1.set_marble_count(self.white_marbles)
            self.p2.set_marble_count(self.black_marbles)
        else:
            self.p1.set_marble_count(self.black_marbles)
            self.p2.set_marble_count(self.white_marbles)

        return True

    def move_right(self, row_input, start):
        # Determine number of marbles to move
        end = start
        while end < len(row_input) and row_input[end] != ' ':
            end += 1

        # Check to see if this will knock our own marble off
        if end == len(row_input) and row_input[end - 1] == row_input[start]:
            return False

        # If our end is the edge, we know a marble is being pushed off.
        if end == len(row_input):
            end -= 1
        temp_row = row_input[:]
        cur = start
        for i in range(start + 1, end + 1):
            temp_row[i] = row_input[cur]
            cur += 1
        temp_row[start] = ' '
        # Copy into input row
        for i in range(len(temp_row)):
            row_input[i] = temp_row[i]
        print(F'   ({start}, {end}) {temp_row}')
        return True

if __name__ == '__main__':
    game = Kuba(('p1', 'W'), ('p2', 'B'))
    game.setupBoard()
    game.showBoard()

    # Implementing right move.
    print(f"1. make_move = {game.make_move('p1', (1, 0), 'R')}")
    game.showBoard()
    game.set_turn('p1')
    print(F'current_turn = {game.current_turn}')

    print(f"2. make_move = {game.make_move('p1', (1, 1), 'R')}")
    game.showBoard()
    game.set_turn('p1')

    print(f"3. make_move = {game.make_move('p1', (1, 2), 'R')}")
    game.showBoard()
    game.set_turn('p1')

    print(f"4. make_move = {game.make_move('p1', (1, 3), 'R')}")
    game.showBoard()
    game.set_turn('p1')

    print(f"5. make_move = {game.make_move('p1', (1, 4), 'R')}")
    game.showBoard()
    game.set_turn('p1')

    game.showGame()
