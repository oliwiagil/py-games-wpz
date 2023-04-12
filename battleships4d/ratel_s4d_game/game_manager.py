import tkinter as tk
from ratel_s4d_game.game_structures import Board4D as R_Board
from ratel_s4d_game.game_structures import GamePhase
from ratel_s4d_game.game_layout import s4d_draw
import ratel_s4d_game.colors_and_text as r_ct


class GameManager:
    def __init__(self, ship_quantities, ship_sizes):
        self.ship_quantities = [int(i) for i in ship_quantities]
        self.ship_sizes = [int(i) for i in ship_sizes]
        if len(self.ship_sizes) != len(self.ship_quantities):
            raise ValueError("Sizes and quantities must be matched into pairs.")
        if len(self.ship_sizes) != len(set(self.ship_sizes)):
            raise ValueError("Sizes for different ship categories must be unique.")
        for i in self.ship_quantities:
            if i <= 0:
                raise ValueError("Ship quantities must be positive.")
        for i in self.ship_sizes:
            if i <= 3:
                raise ValueError("Ship sizes must be greater than 3.")
        self.player_board = R_Board()
        self.bot_board = R_Board()
        self.player_notes = R_Board()
        self.bot_notes = R_Board()
        self.game_phase = GamePhase.INITIAL
        self.phase_state = []
        for i in range(len(self.ship_sizes)):
            self.phase_state = self.phase_state + self.ship_quantities[i] * [self.ship_sizes[i]]
        self.game_window = None
        self.game_frame = None
        self.left_display = None
        self.right_display = None
        self.text_display = None
        self.hint_text = r_ct.place_ship_prompt(self.phase_state[0],
                                                sum(self.ship_quantities) - len(self.phase_state),
                                                sum(self.ship_quantities), False)

    def start(self):
        root = tk.Tk()
        root.title("Ratel's 4 Dimensional Battleships Game")
        window_content = tk.Frame(root)
        window_content.grid(column=0, row=0)
        self.game_window = root
        self.game_frame = window_content

        s4d_draw(self)
        root.mainloop()
