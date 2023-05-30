import numpy as np
import pygame
import const

screen = pygame.display.set_mode(const.size)

def create_board():
    board = np.zeros((const.ROW_COUNT,const.COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[const.ROW_COUNT-1][col] == 0 

def get_next_open_row(board, col):
    for r in range(const.ROW_COUNT):
        if board[r][col] == 0:
            return r 
        
def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):

    for c in range(const.COLUMN_COUNT-3):
        for r in range(const.ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
            
    for c in range(const.COLUMN_COUNT):
        for r in range(const.ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(const.COLUMN_COUNT-3):
        for r in range(const.ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
            
    for c in range(const.COLUMN_COUNT-3):
        for r in range(3, const.ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
            

def draw_board(board):
    for col in range(const.COLUMN_COUNT):
        for r in range(const.ROW_COUNT):
            pygame.draw.rect(screen, const.BLACK, (col*const.SQUARESIZE, r*const.SQUARESIZE+const.SQUARESIZE, const.SQUARESIZE, const.SQUARESIZE))
            pygame.draw.circle(screen, const.WHITE, (int(col*const.SQUARESIZE+const.SQUARESIZE/2), int(r*const.SQUARESIZE+const.SQUARESIZE+const.SQUARESIZE/2)), const.RADIUS)
           
    for col in range(const.COLUMN_COUNT):
        for r in range(const.ROW_COUNT):
            if board[r][col] == 1:
                pygame.draw.circle(screen, const.GREEN, (int(col*const.SQUARESIZE+const.SQUARESIZE/2), const.height-int(r*const.SQUARESIZE+const.SQUARESIZE/2)), const.RADIUS)
            elif board[r][col] == 2:
                pygame.draw.circle(screen, const.PINK, (int(col*const.SQUARESIZE+const.SQUARESIZE/2), const.height-int(r*const.SQUARESIZE+const.SQUARESIZE/2)), const.RADIUS)

    pygame.display.update()
