import tkinter
import os
import json


def new_game():
    """
    Start new game and destroy main_game and game_over window.
    """
    game_over_window.destroy()
    os.system('python main_menu.py')   # running the python command on cmd to execute both windows
    # it must be done this way, as if we simply import it, both windows will open simultaneously.


def quit_game():
    """
    Destroy main_game and game_over window.
    """
    game_over_window.destroy()


with open("end_game.json", encoding="utf-8") as file:
    victory = json.load(file)

game_over_window = tkinter.Tk()
game_over_window.title("Battleships")
game_over_window.resizable(False, False)
game_over_window.configure(padx=10, pady=10)

if victory == "human":
    end_game_text = "VICTORY!"
else:
    end_game_text = "You lost!"

tkinter.Label(game_over_window, text=end_game_text, font=("Rockwell Extra Bold", 22), anchor='center', pady=20, padx=70) \
    .grid(row=0, column=0, columnspan=2, sticky='ew')

new_game_button = tkinter.Button(game_over_window, text="New Game", width=15, command=new_game)
new_game_button.grid(row=1, column=0, padx=30, sticky='s')

quit_button = tkinter.Button(game_over_window, text="Quit", width=15, command=quit_game)
quit_button.grid(row=1, column=1, padx=30, sticky='s')

game_over_window.mainloop()
