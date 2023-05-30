import numpy as np
import pygame
import sys
import math
import functions as f
import const


board = f.create_board()
f.print_board(board)

game_over = False
turn = 0

pygame.init()
f.draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 70)
screen = pygame.display.set_mode(const.size)


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, const.WHITE, (0,0,const.width, const.SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, const.GREEN, (posx, int(const.SQUARESIZE/2)), const.RADIUS)
            else:
                pygame.draw.circle(screen, const.PINK, (posx, int(const.SQUARESIZE/2)), const.RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, const.WHITE, (0,0,const.width, const.SQUARESIZE))

            # #input gracza 1
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/const.SQUARESIZE))

                if f.is_valid_location(board, col):
                    row = f.get_next_open_row(board, col)
                    f.drop_piece(board,row,col,1)

                if f.winning_move(board, 1):
                    label = myfont.render("GRACZ 1 WYGRYWA", 1, const.GREEN)
                    screen.blit(label, (40,10))
                    print("GRACZ 1 WINS")
                    game_over = True


            # #input gracza 2
            else:

                posx = event.pos[0]
                col = int(math.floor(posx/const.SQUARESIZE))

                if f.is_valid_location(board, col):
                    row = f.get_next_open_row(board, col)
                    f.drop_piece(board,row,col,2)

                    if f.winning_move(board, 2):
                        label = myfont.render("GRACZ 2 WYGRYWA", 1, const.PINK)
                        screen.blit(label, (40,10))
                        print("GRACZ 1 WINS")
                        print("GRACZ 2 WINS")
                        game_over = True

            f.print_board(board)
            f.draw_board(board)

            turn = turn + 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)

