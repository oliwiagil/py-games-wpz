from ratel_s4d_game.game_structures import CellState


def pinpoint(board, x, y, z, w, state_set):
    if x < 0 or y < 0 or z < 0 or w < 0 or x > 4 or y > 4 or z > 4 or w > 4:
        return set()
    if board.space[x][y][z][w] in state_set:
        return {(x, y, z, w)}
    return set()


def all_cell_neighbors(board, x, y, z, w, state_set=None):
    if state_set is None:
        state_set = {CellState.EMPTY,
                     CellState.DEAD,
                     CellState.MISSED,
                     CellState.MARKED,
                     CellState.DAMAGED,
                     CellState.FUNCTIONAL}

    def expand3(board0, x0, y0, z0, w0, state_set0):
        return pinpoint(board0, x0, y0, z0, w0 - 1, state_set0) | \
               pinpoint(board0, x0, y0, z0, w0, state_set0) | \
               pinpoint(board0, x0, y0, z0, w0 + 1, state_set0)

    def expand2(board0, x0, y0, z0, w0, state_set0):
        return expand3(board0, x0, y0, z0 - 1, w0, state_set0) | \
               expand3(board0, x0, y0, z0, w0, state_set0) | \
               expand3(board0, x0, y0, z0 + 1, w0, state_set0)

    def expand1(board0, x0, y0, z0, w0, state_set0):
        return expand2(board0, x0, y0 - 1, z0, w0, state_set0) | \
               expand2(board0, x0, y0, z0, w0, state_set0) | \
               expand2(board0, x0, y0 + 1, z0, w0, state_set0)

    def expand0(board0, x0, y0, z0, w0, state_set0):
        return expand1(board0, x0 - 1, y0, z0, w0, state_set0) | \
               expand1(board0, x0, y0, z0, w0, state_set0) | \
               expand1(board0, x0 + 1, y0, z0, w0, state_set0)

    return expand0(board, x, y, z, w, state_set)


def immediate_cell_neighbors(board, x, y, z, w, state_set=None):
    if state_set is None:
        state_set = {CellState.EMPTY,
                     CellState.DEAD,
                     CellState.MISSED,
                     CellState.MARKED,
                     CellState.DAMAGED,
                     CellState.FUNCTIONAL}

    result = (pinpoint(board, x, y, z, w, state_set) |
              pinpoint(board, x - 1, y, z, w, state_set) |
              pinpoint(board, x + 1, y, z, w, state_set) |
              pinpoint(board, x, y - 1, z, w, state_set) |
              pinpoint(board, x, y + 1, z, w, state_set) |
              pinpoint(board, x, y, z - 1, w, state_set) |
              pinpoint(board, x, y, z + 1, w, state_set) |
              pinpoint(board, x, y, z, w - 1, state_set) |
              pinpoint(board, x, y, z, w + 1, state_set))

    return result


def board_wide_search(board, state_set=None):
    if state_set is None:
        state_set = {CellState.EMPTY,
                     CellState.DEAD,
                     CellState.MISSED,
                     CellState.MARKED,
                     CellState.DAMAGED,
                     CellState.FUNCTIONAL}

    result = set()

    for x in range(5):
        for y in range(5):
            for z in range(5):
                for w in range(5):
                    result = result | pinpoint(board, x, y, z, w, state_set)

    return result


def cell_group(board, x, y, z, w, state_set=None):
    if state_set is None:
        state_set = {CellState.EMPTY,
                     CellState.DEAD,
                     CellState.MISSED,
                     CellState.MARKED,
                     CellState.DAMAGED,
                     CellState.FUNCTIONAL}

    result = pinpoint(board, x, y, z, w, state_set)

    while True:
        temp = set()
        for i in result:
            temp = temp | immediate_cell_neighbors(board, *i, state_set)
        if temp == result:
            return result
        result = temp
