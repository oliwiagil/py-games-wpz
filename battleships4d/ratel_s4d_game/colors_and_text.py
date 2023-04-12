from ratel_s4d_game.game_structures import *

# colors for board cells
EMPTY = "#9ec8de"
MISSED = "#666666"
FUNCTIONAL = "#3c5663"
DAMAGED = "#5e080b"
DEAD = "#13071f"
MARKED = "#9c8551"


def place_ship_prompt(current, done, total, started_placing):
    if started_placing:
        return f'Continue placing your ship of size {current} by left-clicking on the marked areas. ' \
               f'You can delete placed cells by right-clicking them. ' \
               f'Right-clicking on a finished ship will delete it and schedule it\'s construction for later. ' \
               f'Placed: {done} of {total}. '
    return f'Left-click on your board display - the one on the left, to start placing a ship of size {current}. ' \
           f'Ships currently placed: {done} of {total}. If you don\'t want to populate the board yourself, click ' \
           f'on any cell on the display on the right. Your board will be then filled randomly. '


def game_over_prompt(result):
    if result == EndState.DRAW:
        return f'The game ended in a draw! All ships destroyed. There\'s no winner. '
    if result == EndState.WIN:
        return f'You won! You destroyed all of the enemy ships. '
    if result == EndState.LOSS:
        return f'You lost! All of your ships were destroyed. '


def battle_prompt():
    return f'Left-click on a cell on the right display to bombard it. Right-click it to place a mark on it. ' \
           f'The bot will attack one of the cells on your board when you attack one of the cells on it\'s. ' \
           f'Whoever destroys all of the ships of the opponent wins. '


def pick_color(game, display, x, y, z, w):
    if display == "left":
        cell_state = game.player_board.space[x][y][z][w]
    elif display == "right":
        cell_state = game.player_notes.space[x][y][z][w]
    else:
        raise ValueError("No such display.")
    if cell_state == CellState.EMPTY:
        return EMPTY
    if cell_state == CellState.MISSED:
        return MISSED
    if cell_state == CellState.FUNCTIONAL:
        return FUNCTIONAL
    if cell_state == CellState.DAMAGED:
        return DAMAGED
    if cell_state == CellState.DEAD:
        return DEAD
    if cell_state == CellState.MARKED:
        return MARKED
