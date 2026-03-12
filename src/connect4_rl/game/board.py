class Board:
    ROWS = 6
    COLS = 7
    EMPTY = 0

    def __init__(self):
        self._board = [[self.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self._turn = 1

    @property
    def board(self):
        return self._board

    @property
    def turn(self):
        return self._turn

    def in_bounds(self, row, col):
        return 0 <= row < self.ROWS and 0 <= col < self.COLS

    def drop_piece(self, col):
        """
        Drop a piece of the current player into de column 'col'.
        Return the row where the piece was places, or None if the move is illegal.
        """
        if not 0 <= col < self.COLS:
            return None

        for row in range(self.ROWS - 1, -1, -1):
            if self._board[row][col] == self.EMPTY:
                self._board[row][col] = self._turn
                return row

        return None

    def switch_turn(self):
        self._turn = 3 - self._turn

    def is_full(self):
        return all(self._board[0][col] != self.EMPTY for col in range(self.COLS))

    def _count_direction(self, row, col, d_row, d_col, player):
        count = 0
        r, c = row + d_row, col + d_col

        while self.in_bounds(r, c) and self._board[r][c] == player:
            count += 1
            r += d_row
            c += d_col

        return count

    def check_win_from(self, row, col, player):
        """
        Check if the player has won by placing a piece at (row, col).
        """
        directions = [
            (0, 1),   # horizontale
            (1, 0),   # verticale
            (1, 1),   # diagonale descendante
            (1, -1),  # diagonale montante
        ]

        for d_row, d_col in directions:
            total = 1
            total += self._count_direction(row, col, d_row, d_col, player)
            total += self._count_direction(row, col, -d_row, -d_col, player)

            if total >= 4:
                return True

        return False

    def play(self, col):
        """
        Play an entire turn for the current player by dropping a piece in column 'col'.
        Return a dict with the result of the move
        """
        player = self._turn
        row = self.drop_piece(col)

        if row is None:
            return {
                "ok": False,
                "reason": "invalid_move",
                "player": player,
            }

        if self.check_win_from(row, col, player):
            return {
                "ok": True,
                "reason": "win",
                "player": player,
                "row": row,
                "col": col,
            }

        if self.is_full():
            return {
                "ok": True,
                "reason": "draw",
                "player": player,
                "row": row,
                "col": col,
            }

        self.switch_turn()
        return {
            "ok": True,
            "reason": "continue",
            "player": player,
            "row": row,
            "col": col,
        }