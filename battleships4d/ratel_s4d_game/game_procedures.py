from ratel_s4d_game.game_structures import *
import random
import ratel_s4d_game.cell_fetchers as cell_fetch
import ratel_s4d_game.colors_and_text as r_ct


def board_click(game, x, y, z, w, click_type):
    if click_type == ["player", "left"]:
        player_left(game, x, y, z, w)
    if click_type == ["player", "right"]:
        player_right(game, x, y, z, w)
    if click_type == ["bot", "left"]:
        bot_left(game, x, y, z, w)
    if click_type == ["bot", "right"]:
        bot_right(game, x, y, z, w)


def player_left(game, x, y, z, w):
    if game.game_phase != GamePhase.INITIAL:
        return
    marked_cells = cell_fetch.board_wide_search(game.player_board, {CellState.MARKED})
    if marked_cells:
        if (x, y, z, w) in marked_cells:
            game.player_board.space[x][y][z][w] = CellState.DAMAGED
            mark_zone = cell_fetch.immediate_cell_neighbors(game.player_board, x, y, z, w, {CellState.EMPTY})
            for i in mark_zone:
                a, b, c, d = i
                game.player_board.space[a][b][c][d] = CellState.MARKED
        else:
            return
    elif cell_fetch.pinpoint(game.player_board, x, y, z, w, {CellState.EMPTY}):
        game.player_board.space[x][y][z][w] = CellState.DAMAGED
        mark_zone = cell_fetch.immediate_cell_neighbors(game.player_board, x, y, z, w, {CellState.EMPTY})
        for i in mark_zone:
            a, b, c, d = i
            game.player_board.space[a][b][c][d] = CellState.MARKED
    else:
        return
    if len(cell_fetch.cell_group(game.player_board, x, y, z, w, {CellState.DAMAGED})) == game.phase_state[0]:
        solidify_ship(game.player_board, x, y, z, w)
        game.phase_state.pop(0)
    if not game.phase_state:
        solidify_board(game.player_board)
        random_setup(game, game.bot_board)
        game.game_phase = GamePhase.BATTLE
        game.phase_state = None
        game.hint_text = r_ct.battle_prompt()
    else:
        game.hint_text = \
            r_ct.place_ship_prompt(game.phase_state[0],
                                   sum(game.ship_quantities) - len(game.phase_state),
                                   sum(game.ship_quantities),
                                   len(cell_fetch.board_wide_search(game.player_board, {CellState.MARKED})) > 0)


def player_right(game, x, y, z, w):
    if game.game_phase != GamePhase.INITIAL:
        return
    if cell_fetch.pinpoint(game.player_board, x, y, z, w, {CellState.DAMAGED}):
        game.player_board.space[x][y][z][w] = CellState.EMPTY
        delete_zone = cell_fetch.board_wide_search(game.player_board, {CellState.MARKED, CellState.MISSED})
        for i in delete_zone:
            a, b, c, d = i
            game.player_board.space[a][b][c][d] = CellState.EMPTY
        exclusion_zone = set()
        ready_ships = cell_fetch.board_wide_search(game.player_board, {CellState.FUNCTIONAL})
        for i in ready_ships:
            exclusion_zone = exclusion_zone | cell_fetch.all_cell_neighbors(game.player_board, *i, {CellState.EMPTY})
        for i in exclusion_zone:
            a, b, c, d = i
            game.player_board.space[a][b][c][d] = CellState.MISSED
        marked_zone = set()
        current_ship = cell_fetch.board_wide_search(game.player_board, {CellState.DAMAGED})
        for i in current_ship:
            marked_zone = marked_zone | cell_fetch.immediate_cell_neighbors(game.player_board, *i, {CellState.EMPTY})
        for i in marked_zone:
            a, b, c, d = i
            game.player_board.space[a][b][c][d] = CellState.MARKED
    elif cell_fetch.pinpoint(game.player_board, x, y, z, w, {CellState.FUNCTIONAL}):
        ship_to_delete = cell_fetch.cell_group(game.player_board, x, y, z, w, {CellState.FUNCTIONAL})
        game.phase_state = [game.phase_state[0]] + [len(ship_to_delete)] + game.phase_state[1:]
        delete_zone = (cell_fetch.board_wide_search(game.player_board, {CellState.MARKED, CellState.MISSED})
                       | ship_to_delete)
        for i in delete_zone:
            a, b, c, d = i
            game.player_board.space[a][b][c][d] = CellState.EMPTY
        exclusion_zone = set()
        ready_ships = cell_fetch.board_wide_search(game.player_board, {CellState.FUNCTIONAL})
        for i in ready_ships:
            exclusion_zone = exclusion_zone | cell_fetch.all_cell_neighbors(game.player_board, *i, {CellState.EMPTY})
        for i in exclusion_zone:
            a, b, c, d = i
            game.player_board.space[a][b][c][d] = CellState.MISSED
        marked_zone = set()
        current_ship = cell_fetch.board_wide_search(game.player_board, {CellState.DAMAGED})
        for i in current_ship:
            marked_zone = marked_zone | cell_fetch.immediate_cell_neighbors(game.player_board, *i, {CellState.EMPTY})
        for i in marked_zone:
            a, b, c, d = i
            game.player_board.space[a][b][c][d] = CellState.MARKED
    game.hint_text = \
        r_ct.place_ship_prompt(game.phase_state[0],
                               sum(game.ship_quantities) - len(game.phase_state),
                               sum(game.ship_quantities),
                               len(cell_fetch.board_wide_search(game.player_board, {CellState.MARKED})) > 0)


def bot_left(game, x, y, z, w):
    if game.game_phase == GamePhase.INITIAL:
        random_player_start(game)
        return
    if game.game_phase != GamePhase.BATTLE:
        return
    player_shot(game, x, y, z, w)
    bot_shot(game)
    check_game_ended(game)
    if game.game_phase == GamePhase.CONCLUSION:
        game.hint_text = r_ct.game_over_prompt(game.phase_state)
    else:
        game.hint_text = r_ct.battle_prompt()


def bot_right(game, x, y, z, w):
    if game.game_phase == GamePhase.INITIAL:
        random_player_start(game)
        return
    if game.game_phase != GamePhase.BATTLE:
        return
    if game.player_notes.space[x][y][z][w] == CellState.EMPTY:
        game.player_notes.space[x][y][z][w] = CellState.MARKED
    elif game.player_notes.space[x][y][z][w] == CellState.MARKED:
        game.player_notes.space[x][y][z][w] = CellState.EMPTY


def random_player_start(game):
    random_setup(game, game.player_board)
    random_setup(game, game.bot_board)
    game.game_phase = GamePhase.BATTLE
    game.phase_state = None
    game.hint_text = r_ct.battle_prompt()


def solidify_board(board):
    blocked_space = cell_fetch.board_wide_search(board, {CellState.MISSED})
    for i in blocked_space:
        board.space[i[0]][i[1]][i[2]][i[3]] = CellState.EMPTY


def solidify_ship(board, x, y, z, w):
    ship_body = cell_fetch.cell_group(board, x, y, z, w, {CellState.DAMAGED})
    blocked_space = set()
    for i in ship_body:
        blocked_space = blocked_space | cell_fetch.all_cell_neighbors(board, *i, {CellState.EMPTY, CellState.MARKED})
        board.space[i[0]][i[1]][i[2]][i[3]] = CellState.FUNCTIONAL
    for i in blocked_space:
        board.space[i[0]][i[1]][i[2]][i[3]] = CellState.MISSED


def random_setup(game, board):
    def place_ship():
        position = random_coordinates()
        while len(cell_fetch.cell_group(board, *position, {CellState.EMPTY})) < temp_state[0]:
            position = random_coordinates()
        board.space[position[0]][position[1]][position[2]][position[3]] = CellState.DAMAGED
        mark_space = cell_fetch.immediate_cell_neighbors(board, *position, {CellState.EMPTY})
        for j in mark_space:
            board.space[j[0]][j[1]][j[2]][j[3]] = CellState.MARKED
        while len(cell_fetch.cell_group(board, *position, {CellState.DAMAGED})) < temp_state[0]:
            position = random_coordinates()
            while not cell_fetch.pinpoint(board, *position, {CellState.MARKED}):
                position = random_coordinates()
            board.space[position[0]][position[1]][position[2]][position[3]] = CellState.DAMAGED
            mark_space = cell_fetch.immediate_cell_neighbors(board, *position, {CellState.EMPTY})
            for j in mark_space:
                board.space[j[0]][j[1]][j[2]][j[3]] = CellState.MARKED
        solidify_ship(board, *position)
        temp_state.pop(0)

    def storm_search():
        for j in cell_fetch.board_wide_search(board, {CellState.EMPTY}):
            if len(cell_fetch.cell_group(board, *j, {CellState.EMPTY})) >= temp_state[0]:
                return False
        return True

    def try_setup():
        while temp_state:
            if storm_search():
                return False
            place_ship()
        return True

    while True:
        cells = cell_fetch.board_wide_search(board)
        for i in cells:
            board.space[i[0]][i[1]][i[2]][i[3]] = CellState.EMPTY
        temp_state = []
        for i in range(len(game.ship_sizes)):
            temp_state = temp_state + game.ship_quantities[i] * [game.ship_sizes[i]]
        if try_setup():
            solidify_board(board)
            return


def player_shot(game, x, y, z, w):
    if game.bot_board.space[x][y][z][w] == CellState.EMPTY:
        game.bot_board.space[x][y][z][w] = CellState.MISSED
    if game.bot_board.space[x][y][z][w] == CellState.FUNCTIONAL:
        game.bot_board.space[x][y][z][w] = CellState.DAMAGED
        try_sink(game.bot_board, x, y, z, w)

    damaged_cells = cell_fetch.board_wide_search(game.bot_board, {CellState.DAMAGED})
    for i in damaged_cells:
        x, y, z, w = i
        game.player_notes.space[x][y][z][w] = CellState.DAMAGED
    dead_cells = cell_fetch.board_wide_search(game.bot_board, {CellState.DEAD})
    for i in dead_cells:
        x, y, z, w = i
        game.player_notes.space[x][y][z][w] = CellState.DEAD
    missed_cells = cell_fetch.board_wide_search(game.bot_board, {CellState.MISSED})
    for i in missed_cells:
        x, y, z, w = i
        game.player_notes.space[x][y][z][w] = CellState.MISSED


def bot_shot(game):
    position = random_coordinates()
    damaged_section = cell_fetch.board_wide_search(game.bot_notes, {CellState.DAMAGED})
    if damaged_section:
        target_set = set()
        for i in damaged_section:
            target_set = target_set | cell_fetch.immediate_cell_neighbors(game.bot_notes, *i, {CellState.EMPTY})
        while not (position in target_set):
            position = random_coordinates()
    else:
        while (sum(position) % 2) or (not cell_fetch.pinpoint(game.bot_notes, *position, {CellState.EMPTY})):
            position = random_coordinates()

    x, y, z, w = position
    if game.player_board.space[x][y][z][w] == CellState.EMPTY:
        game.player_board.space[x][y][z][w] = CellState.MISSED
    if game.player_board.space[x][y][z][w] == CellState.FUNCTIONAL:
        game.player_board.space[x][y][z][w] = CellState.DAMAGED
        try_sink(game.player_board, *position)

    damaged_cells = cell_fetch.board_wide_search(game.player_board, {CellState.DAMAGED})
    for i in damaged_cells:
        x, y, z, w = i
        game.bot_notes.space[x][y][z][w] = CellState.DAMAGED
    dead_cells = cell_fetch.board_wide_search(game.player_board, {CellState.DEAD})
    for i in dead_cells:
        x, y, z, w = i
        game.bot_notes.space[x][y][z][w] = CellState.DEAD
    missed_cells = cell_fetch.board_wide_search(game.player_board, {CellState.MISSED})
    for i in missed_cells:
        x, y, z, w = i
        game.bot_notes.space[x][y][z][w] = CellState.MISSED

    dead_section = cell_fetch.board_wide_search(game.bot_notes, {CellState.DEAD})
    mark_space = set()
    for i in dead_section:
        mark_space = mark_space | cell_fetch.all_cell_neighbors(game.bot_notes, *i, {CellState.EMPTY})
    for i in mark_space:
        x, y, z, w = i
        game.bot_notes.space[x][y][z][w] = CellState.MARKED


def try_sink(board, x, y, z, w):
    ship_body = cell_fetch.cell_group(board, x, y, z, w, {CellState.FUNCTIONAL, CellState.DAMAGED})
    damaged_part = cell_fetch.cell_group(board, x, y, z, w, {CellState.DAMAGED})
    if len(ship_body) == len(damaged_part):
        for i in ship_body:
            board.space[i[0]][i[1]][i[2]][i[3]] = CellState.DEAD


def check_game_ended(game):
    if (not cell_fetch.board_wide_search(game.player_board, {CellState.FUNCTIONAL})) \
            or (not cell_fetch.board_wide_search(game.bot_board, {CellState.FUNCTIONAL})):
        game.game_phase = GamePhase.CONCLUSION
        if cell_fetch.board_wide_search(game.player_board, {CellState.FUNCTIONAL}):
            game.phase_state = EndState.WIN
            return
        if cell_fetch.board_wide_search(game.bot_board, {CellState.FUNCTIONAL}):
            game.phase_state = EndState.LOSS
            return
        game.phase_state = EndState.DRAW


def random_coordinates():
    return random.randrange(5), random.randrange(5), random.randrange(5), random.randrange(5)
