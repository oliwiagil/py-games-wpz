import ratel_s4d_game.game_manager as r_gm
import ratel_s4d_game.game_structures as game_structs
import ratel_s4d_game.cell_fetchers as cell_fetch
import os


if __name__ == '__main__':
    game = r_gm.GameManager([2, 2, 4, 4], [15, 10, 5, 4])
    game.start()
    
    n_friendly_surviving = len(cell_fetch.board_wide_search(game.player_board, {game_structs.CellState.FUNCTIONAL}))
    n_enemy_surviving = len(cell_fetch.board_wide_search(game.bot_board, {game_structs.CellState.FUNCTIONAL}))
    
    bonus = {
        game_structs.EndState.LOSS: -100,
        game_structs.EndState.DRAW: 0,
        game_structs.EndState.WIN: 100
    }
    
    if game.game_phase == game_structs.GamePhase.CONCLUSION:
        score = n_friendly_surviving - n_enemy_surviving + bonus[game.phase_state]
        prev_score = -1_000_000
        try:
            with open(os.path.dirname(__file__) + '/score.txt', 'r') as score_file:
                prev_score = int(score_file.read())
            with open(os.path.dirname(__file__) + '/score.txt', 'w') as score_file:
                score_file.write(str(max(score, prev_score)))
        except:
            with open(os.path.dirname(__file__) + '/score.txt', 'w') as score_file:
                score_file.write(str(score))
    
