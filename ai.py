"""ai.py - Fungsi evaluasi dan MiniMax + Alpha-Beta Pruning."""

from board import (apply_move, count_discs, game_over, get_valid_moves)

WEIGHTS = [
    [100, -20, 10,  5,  5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [ 10,  -2, -1, -1, -1, -1,  -2,  10],
    [  5,  -2, -1, -1, -1, -1,  -2,   5],
    [  5,  -2, -1, -1, -1, -1,  -2,   5],
    [ 10,  -2, -1, -1, -1, -1,  -2,  10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10,  5,  5, 10, -20, 100],
]


def evaluate(board, player):
    """Fungsi evaluasi dari sudut pandang `player`."""
    black, white = count_discs(board)
    opp = -player

    # Kondisi akhir permainan: hanya selisih disk yang penting
    if game_over(board):
        diff = (black - white) * player
        return 10000 * (1 if diff > 0 else -1 if diff < 0 else 0)

    # 1. Skor posisi (weighted matrix)
    positional = sum(WEIGHTS[r][c] * board[r][c] * player
                     for r in range(8) for c in range(8))

    # 2. Mobility: selisih jumlah langkah legal
    my_moves = len(get_valid_moves(board, player))
    opp_moves = len(get_valid_moves(board, opp))
    mobility = 5 * (my_moves - opp_moves)

    #example
    #player 8 langkah, lawan 3 langkah
    #5 x (8-3)= +25 >> nilai ini dipakai oleh minimax untuk pertimbangan langkah

    # 3. Selisih disk, bobotnya naik di akhir permainan
    total = black + white
    disc_diff = (black - white) * player
    disc_score = disc_diff * (total / 64) * 2

    return positional + mobility + disc_score

#example
#positional = +40
#mobility   = +25
#disc_score =  +3
#-------------------
#skor akhir = +68


def alphabeta(board, depth, alpha, beta, current, ai):
    """
    current : pemain yang sedang giliran (BLACK / WHITE)
    ai      : pemain yang dimaksimalkan skornya
    return  : (skor, langkah_terbaik)
    """
    if depth == 0 or game_over(board):
        return evaluate(board, ai), None

    moves = get_valid_moves(board, current)

    # Pass: pemain tidak punya langkah, giliran pindah ke lawan
    if not moves:
        score, _ = alphabeta(board, depth - 1, alpha, beta, -current, ai)
        return score, None

    # Move ordering: coba kotak bernilai tinggi dulu supaya pruning lebih efektif
    moves.sort(key=lambda m: WEIGHTS[m[0]][m[1]], reverse=True)

    best_move = None
    if current == ai:  # MAX
        value = float('-inf')
        for move in moves:
            new_board = apply_move(board, move, current)
            score, _ = alphabeta(new_board, depth - 1, alpha, beta, -current, ai)
            if score > value: 
                value, best_move = score, move
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # pruning
        return value, best_move
    else:              # MIN
        value = float('inf')
        for move in moves:
            new_board = apply_move(board, move, current)
            score, _ = alphabeta(new_board, depth - 1, alpha, beta, -current, ai)
            if score < value:
                value, best_move = score, move
            beta = min(beta, value)
            if alpha >= beta:
                break  # pruning
        return value, best_move


def ai_choose_move(board, player, depth):
    _, move = alphabeta(board, depth, float('-inf'), float('inf'), player, player)
    return move