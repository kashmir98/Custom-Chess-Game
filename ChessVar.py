# Author: Musa Rangrez
# GitHub Username: kashmir98
# Date: 12/08/24
# Description: This project implements a custom chess game where players can only see with their own pieces,
# manage their potential moves, and must navigate through uncharted terrain to capture opponent's pieces.

class ChessVar:
    """This class implements the chess game logic, manages turns, and handles visibility rules."""

    def __init__(self):
        """Sets up the game by initializing the chess board, setting the starting game state, and deciding who moves first."""

        self._board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self._game_state = 'UNFINISHED'
        self._turn = 'white'

    def get_game_state(self):
        """Provides the current status of the game – 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'"""

        return self._game_state

    def get_board(self, perspective):
        """Returns the board depiction from the given perspective. Perspective can be 'white', 'black', or
        'audience' to indicate the view."""

        if perspective == 'audience':
            return self._board
        elif perspective == 'white':
            return self._get_player_view('white')
        elif perspective == 'black':
            return self._get_player_view('black')

    def make_move(self, from_square, to_square):
        """Moves a piece from one square to another if it's a valid move. Create a starting position and a
        target ending. Use boolean to return true/false to indicate validity."""

        if self._game_state != 'UNFINISHED':
            return False

        start_pos = self._convert_to_index(from_square)
        end_pos = self._convert_to_index(to_square)

        # We will validate the move before proceeding
        if not self._validate_move(start_pos, end_pos):
            return False

        # Updates the board and game state after a valid move
        self._update_board(start_pos, end_pos)
        self._check_game_state()
        self._switch_turn()
        return True

    def _get_player_view(self, color):
        """Adjusts the board to only show pieces visible to the specified player (white or black)."""

        view = [['*' for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                piece = self._board[row][col]
                if piece == ' ':  # Empty spaces are always visible
                    view[row][col] = ' '
                elif (color == 'white' and piece.isupper()) or (color == 'black' and piece.islower()):
                    view[row][col] = piece  # Player's own pieces are visible
                elif self._can_be_captured((row, col), color):
                    view[row][col] = piece  # Opponent's pieces that can be captured are visible
        return view

    def _can_be_captured(self, position, color):
        """Checks if a piece at a given position can be captured by the opposing player.
        In this case, capturing a piece means it is within the movement range of an opponent's piece."""

        row, col = position
        piece = self._board[row][col]
        if piece == ' ':  # Empty spaces can't be captured
            return False

        directions = self._get_piece_directions(piece)
        for direction in directions:
            r, c = row + direction[0], col + direction[1]
            while 0 <= r < 8 and 0 <= c < 8:
                if self._board[r][c] != ' ':  # Stop at the first non-empty square
                    if (color == 'white' and self._board[r][c].islower()) or (color == 'black' and self._board[r][c].isupper()):
                        return True  # The piece can be captured
                    break
                r += direction[0]
                c += direction[1]
        return False

    def _validate_move(self, start_pos, end_pos):
        """Checks if the move from start to end is valid."""

        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self._board[start_row][start_col]

        # Checks if the start position is valid
        if piece == ' ':  # No piece to move
            return False
        if (self._turn == 'white' and piece.islower()) or (self._turn == 'black' and piece.isupper()):
            return False  # Not the player's turn for this piece

        # Checks if the end position is within the board
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        # Validate based on the piece's movement rules
        directions = self._get_piece_directions(piece)
        valid = any((start_row + d[0] == end_row and start_col + d[1] == end_col) for d in directions)
        return valid

    def _get_piece_directions(self, piece):
        """Gets the allowed movement configuration for a specific piece."""

        directions = {
            'p': [(1, 0), (1, 1), (1, -1)],
            'P': [(-1, 0), (-1, 1), (-1, -1)],
            'r': [(1, 0), (0, 1), (-1, 0), (0, -1)],
            'R': [(1, 0), (0, 1), (-1, 0), (0, -1)],
            'n': [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)],
            'N': [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)],
            'b': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
            'B': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
            'q': [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],
            'Q': [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],
            'k': [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],
            'K': [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        }
        return directions.get(piece.lower(), [])

    def _update_board(self, start_pos, end_pos):
        """Updates the board to show the move."""

        piece = self._board[start_pos[0]][start_pos[1]]
        self._board[start_pos[0]][start_pos[1]] = ' '
        self._board[end_pos[0]][end_pos[1]] = piece

    def _check_game_state(self):
        """Updates the game state to reflect whether one player's king has been captured."""

        kings = [any('k' in row for row in self._board), any('K' in row for row in self._board)]
        if not kings[0]:
            self._game_state = 'WHITE_WON'
        elif not kings[1]:
            self._game_state = 'BLACK_WON'

    def _switch_turn(self):
        """Alternates the turn between white and black players."""

        self._turn = 'black' if self._turn == 'white' else 'white'

    def _convert_to_index(self, square):
        """Converts a chess square in algebraic notation to board indices."""

        col = ord(square[0]) - ord('a')
        row = 8 - int(square[1])
        return row, col
