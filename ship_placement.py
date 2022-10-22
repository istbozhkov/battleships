import tkinter
import ship_setup
import board
import btn
import os

# TODO protect variable by adding _ at the start
# TODO add validation checks for all variables


def run_game():
    """
    Run main game module and destroy ship placement window.
    """
    ship_setup.mainWindow.destroy()
    os.system('python main_game.py')   # running the python command on cmd to execute both windows
    # it must be done this way, as if we simply import it, both windows will open simultaneously.


human_board = board.SetUpBoard(size=ship_setup.board_size, window=ship_setup.mainWindow,
                               ship_configuration=ship_setup.ship_configuration, button_class=btn.Btn)
human_board.draw_placement_field(run_game)

ship_setup.mainWindow.mainloop()
