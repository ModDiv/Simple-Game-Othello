"""main.py - Tampilan pygame dan game loop. Jalankan file ini."""

import pygame

from board import (BLACK, WHITE, apply_move, count_discs, game_over,
                   get_valid_moves, new_board)
from ai import ai_choose_move

CELL = 80
BOARD_SIZE = CELL * 8
BAR_HEIGHT = 70
WIDTH, HEIGHT = BOARD_SIZE, BOARD_SIZE + BAR_HEIGHT

GREEN = (34, 139, 34)
DARK_GREEN = (0, 90, 0)
BLACK_C = (20, 20, 20)
WHITE_C = (240, 240, 240)
HINT = (200, 200, 60)
BAR_BG = (40, 40, 40)

HUMAN, AI = BLACK, WHITE
DEPTH_LABEL = {1: "Mudah", 3: "Sedang", 4: "Sulit"}


def draw_board(screen, font, board, valid_moves, turn, depth, message, over):
    screen.fill(GREEN)

    # Garis grid
    for i in range(9):
        pygame.draw.line(screen, DARK_GREEN, (i * CELL, 0), (i * CELL, BOARD_SIZE), 2)
        pygame.draw.line(screen, DARK_GREEN, (0, i * CELL), (BOARD_SIZE, i * CELL), 2)

    # Disk
    for r in range(8):
        for c in range(8):
            center = (c * CELL + CELL // 2, r * CELL + CELL // 2)
            if board[r][c] == BLACK:
                pygame.draw.circle(screen, BLACK_C, center, CELL // 2 - 8)
            elif board[r][c] == WHITE:
                pygame.draw.circle(screen, WHITE_C, center, CELL // 2 - 8)

    # Petunjuk langkah legal untuk pemain
    if not over and turn == HUMAN:
        for r, c in valid_moves:
            center = (c * CELL + CELL // 2, r * CELL + CELL // 2)
            pygame.draw.circle(screen, HINT, center, 8)

    # Bar informasi
    pygame.draw.rect(screen, BAR_BG, (0, BOARD_SIZE, WIDTH, BAR_HEIGHT))
    black, white = count_discs(board)
    score_text = (f"Kamu (Hitam): {black}   AI (Putih): {white}   "
                  f"Level: {DEPTH_LABEL.get(depth, depth)}")
    screen.blit(font.render(score_text, True, WHITE_C), (10, BOARD_SIZE + 8))

    if over:
        if black > white:
            status = "Game selesai: Kamu menang! (R = main lagi)"
        elif white > black:
            status = "Game selesai: AI menang! (R = main lagi)"
        else:
            status = "Game selesai: Seri! (R = main lagi)"
    elif message:
        status = message
    else:
        status = "Giliranmu" if turn == HUMAN else "AI sedang berpikir..."
    screen.blit(font.render(status, True, HINT), (10, BOARD_SIZE + 38))


def main(depth=3):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Othello - MiniMax + Alpha-Beta")
    font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()

    board = new_board()
    turn = HUMAN
    message = ""
    running = True

    while running:
        over = game_over(board)
        valid_moves = get_valid_moves(board, turn) if not over else []

        # Pass otomatis jika pemain yang giliran tidak punya langkah
        if not over and not valid_moves:
            who = "Kamu" if turn == HUMAN else "AI"
            message = f"{who} tidak punya langkah, giliran dilewati"
            turn = -turn
            valid_moves = get_valid_moves(board, turn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board, turn, message = new_board(), HUMAN, ""
                elif event.key == pygame.K_1:
                    depth = 1
                elif event.key == pygame.K_2:
                    depth = 3
                elif event.key == pygame.K_3:
                    depth = 4
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == HUMAN and not over:
                x, y = event.pos
                if y < BOARD_SIZE:
                    r, c = y // CELL, x // CELL
                    if (r, c) in valid_moves:
                        board = apply_move(board, (r, c), HUMAN)
                        turn = AI
                        message = ""

        draw_board(screen, font, board, valid_moves, turn, depth, message, over)
        pygame.display.flip()

        # Giliran AI (layar digambar dulu supaya terlihat "berpikir")
        if turn == AI and not over and valid_moves:
            move = ai_choose_move(board, AI, depth)
            if move:
                board = apply_move(board, move, AI)
            turn = HUMAN

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main(depth=3)