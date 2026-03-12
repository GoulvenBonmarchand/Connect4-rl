import pytest

from connect4_rl.game.board import Board

def test_board_initialization():
    board = Board()

    assert board.ROWS == 6
    assert board.COLS == 7
    assert board.EMPTY == 0
    assert len(board.board) == 6
    assert all(len(row) == 7 for row in board.board)
    assert all(cell == 0 for row in board.board for cell in row)
    assert board.turn == 1


def test_in_bounds_valid_coordinates():
    board = Board()

    assert board.in_bounds(0, 0) is True
    assert board.in_bounds(5, 6) is True


@pytest.mark.parametrize(
    "row, col",
    [(-1, 0), (0, -1), (6, 0), (0, 7), (6, 7), (-1, -1)],
)
def test_in_bounds_invalid_coordinates(row, col):
    board = Board()

    assert board.in_bounds(row, col) is False


def test_drop_piece_returns_bottom_row():
    board = Board()

    row = board.drop_piece(3)

    assert row == 5
    assert board.board[5][3] == 1


def test_drop_piece_stacks_up_in_same_column():
    board = Board()

    row1 = board.drop_piece(2)
    row2 = board.drop_piece(2)
    row3 = board.drop_piece(2)

    assert row1 == 5
    assert row2 == 4
    assert row3 == 3

    # drop_piece ne change pas le tour tout seul
    assert board.board[5][2] == 1
    assert board.board[4][2] == 1
    assert board.board[3][2] == 1


@pytest.mark.parametrize("col", [-1, 7, 100])
def test_drop_piece_invalid_column_returns_none(col):
    board = Board()

    row = board.drop_piece(col)

    assert row is None
    assert all(cell == 0 for row in board.board for cell in row)
    assert board.turn == 1


def test_drop_piece_full_column_returns_none():
    board = Board()

    for _ in range(board.ROWS):
        assert board.drop_piece(0) is not None

    assert board.drop_piece(0) is None


def test_switch_turn_changes_player():
    board = Board()

    assert board.turn == 1
    board.switch_turn()
    assert board.turn == 2
    board.switch_turn()
    assert board.turn == 1


def test_is_full_false_on_empty_board():
    board = Board()

    assert board.is_full() is False


def test_is_full_true_when_top_row_has_no_empty_cell():
    board = Board()

    for col in range(board.COLS):
        for _ in range(board.ROWS):
            board.drop_piece(col)

    assert board.is_full() is True


def test_count_direction_horizontal():
    board = Board()
    board._board[5][1] = 1
    board._board[5][2] = 1
    board._board[5][3] = 1

    count = board._count_direction(5, 0, 0, 1, 1)

    assert count == 3


def test_count_direction_vertical():
    board = Board()
    board._board[3][2] = 2
    board._board[4][2] = 2
    board._board[5][2] = 2

    count = board._count_direction(2, 2, 1, 0, 2)

    assert count == 3


def test_count_direction_diagonal_descending():
    board = Board()
    board._board[2][1] = 1
    board._board[3][2] = 1
    board._board[4][3] = 1

    count = board._count_direction(1, 0, 1, 1, 1)

    assert count == 3


def test_count_direction_returns_zero_when_no_match():
    board = Board()
    board._board[5][1] = 2
    board._board[5][2] = 2

    count = board._count_direction(5, 0, 0, 1, 1)

    assert count == 0


def test_check_win_from_horizontal():
    board = Board()
    player = 1

    board._board[5][0] = player
    board._board[5][1] = player
    board._board[5][2] = player
    board._board[5][3] = player

    assert board.check_win_from(5, 3, player) is True


def test_check_win_from_vertical():
    board = Board()
    player = 2

    board._board[2][4] = player
    board._board[3][4] = player
    board._board[4][4] = player
    board._board[5][4] = player

    assert board.check_win_from(2, 4, player) is True


def test_check_win_from_diagonal_descending():
    board = Board()
    player = 1

    board._board[2][0] = player
    board._board[3][1] = player
    board._board[4][2] = player
    board._board[5][3] = player

    assert board.check_win_from(5, 3, player) is True


def test_check_win_from_diagonal_ascending():
    board = Board()
    player = 2

    board._board[5][0] = player
    board._board[4][1] = player
    board._board[3][2] = player
    board._board[2][3] = player

    assert board.check_win_from(2, 3, player) is True


def test_check_win_from_false_when_not_four_in_a_row():
    board = Board()
    player = 1

    board._board[5][0] = player
    board._board[5][1] = player
    board._board[5][2] = player

    assert board.check_win_from(5, 2, player) is False


def test_play_invalid_move():
    board = Board()

    result = board.play(-1)

    assert result == {
        "ok": False,
        "reason": "invalid_move",
        "player": 1,
    }
    assert board.turn == 1


def test_play_continue_returns_expected_dict_and_switches_turn():
    board = Board()

    result = board.play(3)

    assert result == {
        "ok": True,
        "reason": "continue",
        "player": 1,
        "row": 5,
        "col": 3,
    }
    assert board.board[5][3] == 1
    assert board.turn == 2


def test_play_win_horizontal():
    board = Board()

    # Prépare trois pions du joueur 1 sur la ligne du bas
    board._board[5][0] = 1
    board._board[5][1] = 1
    board._board[5][2] = 1
    board._turn = 1

    result = board.play(3)

    assert result == {
        "ok": True,
        "reason": "win",
        "player": 1,
        "row": 5,
        "col": 3,
    }
    assert board.turn == 1  # pas de switch après victoire


def test_play_draw():
    board = Board()

    # Plateau presque plein, sans gagnant, avec une seule case vide en haut de la colonne 0
    board._board = [
    [0, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 1, 2],
    ]
    board._turn = 1

    result = board.play(0)

    assert result == {
        "ok": True,
        "reason": "draw",
        "player": 1,
        "row": 0,
        "col": 0,
    }
    assert board.turn == 1  # pas de switch après nul