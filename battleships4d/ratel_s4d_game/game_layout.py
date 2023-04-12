import ratel_s4d_game.colors_and_text as r_ct
import tkinter as tk
from ratel_s4d_game.game_procedures import board_click


def s4d_draw(game):
    root = game.game_window
    window_content = game.game_frame
    window_content.grid_forget()
    window_content = tk.Frame(root)

    board_panel = tk.Frame(window_content)

    player_display = tk.Frame(board_panel)
    bot_display = tk.Frame(board_panel)

    player_display_segmented = [[tk.Frame(player_display) for _ in range(5)] for _ in range(5)]
    bot_display_segmented = [[tk.Frame(bot_display) for _ in range(5)] for _ in range(5)]

    player_display_cells = [[[[tk.Canvas(player_display_segmented[x][y], width=20, height=20, bg=r_ct.EMPTY)
                               for _ in range(5)]
                              for _ in range(5)]
                             for y in range(5)]
                            for x in range(5)]
    game.left_display = player_display_cells

    bot_display_cells = [[[[tk.Canvas(bot_display_segmented[x][y], width=20, height=20, bg=r_ct.EMPTY)
                            for _ in range(5)]
                           for _ in range(5)]
                          for y in range(5)]
                         for x in range(5)]
    game.right_display = bot_display_cells

    def handler_provider(n_game, n_x, n_y, n_z, n_w, click_type):
        def result(_):
            # """
            print(f'Click registered: {str(click_type)} at {n_x} {n_y} {n_z} {n_w} in game phase: {n_game.game_phase},'
                  f' phase state: {n_game.phase_state}.')
            # """
            board_click(n_game, n_x, n_y, n_z, n_w, click_type)
            s4d_redraw(n_game)
        return result

    for x in range(5):
        for y in range(5):
            for z in range(5):
                for w in range(5):
                    player_display_cells[x][y][z][w].bind(
                        "<Button-1>", handler_provider(game, x, y, z, w, ["player", "left"]))
                    player_display_cells[x][y][z][w].bind(
                        "<Button-2>", handler_provider(game, x, y, z, w, ["player", "right"]))
                    player_display_cells[x][y][z][w].bind(
                        "<Button-3>", handler_provider(game, x, y, z, w, ["player", "right"]))
                    bot_display_cells[x][y][z][w].bind(
                        "<Button-1>", handler_provider(game, x, y, z, w, ["bot", "left"]))
                    bot_display_cells[x][y][z][w].bind(
                        "<Button-2>", handler_provider(game, x, y, z, w, ["bot", "right"]))
                    bot_display_cells[x][y][z][w].bind(
                        "<Button-3>", handler_provider(game, x, y, z, w, ["bot", "right"]))

                    player_display_cells[x][y][z][w].grid(column=z, row=w, padx=1, pady=1)
                    bot_display_cells[x][y][z][w].grid(column=z, row=w, padx=1, pady=1)
            player_display_segmented[x][y].grid(column=x, row=y, padx=2, pady=2)
            bot_display_segmented[x][y].grid(column=x, row=y, padx=2, pady=2)
    player_display.grid(column=0, row=0, padx=10, pady=5)
    bot_display.grid(column=1, row=0, padx=10, pady=5)
    board_panel.grid(column=0, row=0)

    text_display = tk.Label(window_content, text=game.hint_text)
    game.text_display = text_display
    text_display.grid(column=0, row=1)

    window_content.grid(column=0, row=0)


def s4d_redraw(game):
    for x in range(5):
        for y in range(5):
            for z in range(5):
                for w in range(5):
                    game.left_display[x][y][z][w].configure(bg=r_ct.pick_color(game, "left", x, y, z, w))
                    game.right_display[x][y][z][w].configure(bg=r_ct.pick_color(game, "right", x, y, z, w))
    game.text_display.configure(text=game.hint_text)
