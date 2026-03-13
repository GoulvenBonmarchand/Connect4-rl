import random

def smart_agent(board, player):
    """
    Agent with simple priorities:
    1. Play a winning move if possible
    2. Block opponent's winning move if possible
    3. Otherwise play randomly
    """

    def drop_piece(current_board, col, who):
        next_board = [row[:] for row in current_board]
        for row in range(5, -1, -1):
            if next_board[row][col] == 0:
                next_board[row][col] = who
                return next_board, row
        return next_board, None

    def in_bounds(row, col):
        return 0 <= row < 6 and 0 <= col < 7

    def count_direction(current_board, row, col, d_row, d_col, who):
        count = 0
        r, c = row + d_row, col + d_col

        while in_bounds(r, c) and current_board[r][c] == who:
            count += 1
            r += d_row
            c += d_col

        return count

    def check_win_move(col, who):
        next_board, row = drop_piece(board, col, who)
        if row is None:
            return False

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]

        for d_row, d_col in directions:
            total = 1
            total += count_direction(next_board, row, col, d_row, d_col, who)
            total += count_direction(next_board, row, col, -d_row, -d_col, who)

            if total >= 4:
                return True

        return False

    valid_moves = [col for col in range(7) if board[0][col] == 0]

    #Noramaly useless, but in case it will avoid crash
    if not valid_moves:
        return None

    for col in valid_moves:
        if check_win_move(col, player):
            return col

    for col in valid_moves:
        if check_win_move(col, 3 - player):
            return col

    return random.choice(valid_moves)