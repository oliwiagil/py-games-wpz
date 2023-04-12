import ratel_s4d_game.game_manager as r_gm


if __name__ == '__main__':
    game = r_gm.GameManager([2, 2, 4, 4], [15, 10, 5, 4])
    game.start()
