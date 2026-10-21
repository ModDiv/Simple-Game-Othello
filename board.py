"""board.py - Logika papan Othello (tanpa pygame)."""

EMPTY, BLACK, WHITE = 0, 1, -1
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]


def new_board():
    """Papan 8x8 dengan 4 disk awal di tengah."""
    board = [[EMPTY] * 8 for _ in range(8)]
    board[3][3], board[4][4] = WHITE, WHITE
    board[3][4], board[4][3] = BLACK, BLACK
    return board


def on_board(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def flips_for_move(board, r, c, player):
    """Daftar disk lawan yang terbalik jika player menaruh disk di (r, c)."""
    if board[r][c] != EMPTY:
        return []
    flips = []
    for dr, dc in DIRECTIONS:
        line = []
        rr, cc = r + dr, c + dc
        while on_board(rr, cc) and board[rr][cc] == -player:
            line.append((rr, cc))
            rr += dr
            cc += dc
        if line and on_board(rr, cc) and board[rr][cc] == player:
            flips.extend(line)
    return flips


def get_valid_moves(board, player):
    return [(r, c) for r in range(8) for c in range(8)
            if flips_for_move(board, r, c, player)]


def apply_move(board, move, player):
    """Mengembalikan papan baru setelah langkah dijalankan."""
    r, c = move
    new = [row[:] for row in board]
    for fr, fc in flips_for_move(board, r, c, player):
        new[fr][fc] = player
    new[r][c] = player
    return new


def count_discs(board):
    black = sum(row.count(BLACK) for row in board)
    white = sum(row.count(WHITE) for row in board)
    return black, white


def game_over(board):
    return not get_valid_moves(board, BLACK) and not get_valid_moves(board, WHITE)