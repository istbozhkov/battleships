import tkinter
import os
import json


def run_ship_placement(difficulty: str, size: int, ships: str) -> None:
    """
    Save settings to a json file, run ship placement module and destroy main menu window.
    :param filename: filename of main game module
    """
    # Converting ships sizes from string to list of integers:
    ships_list = [int(i) for i in ships.split(", ")]
    settings = {
        "difficulty level": difficulty,
        "board size": size,
        "ship configuration": ships_list
    }
    # Saving settings to a json file:
    with open('config.json', 'w', encoding="utf-8") as config:
        json.dump(settings, config)
    main_menu_window.destroy()
    os.system("python ship_placement.py")   # running the python command on cmd to execute both windows
    # it must be done this way, as if we simply import it, both windows will open simultaneously.


# Defining board sizes:
board_size_option1_int = 6
board_size_option2_int = 8
board_size_option3_int = 10
board_size_option1_text = str(board_size_option1_int) + "x" + str(board_size_option1_int)
board_size_option2_text = str(board_size_option2_int) + "x" + str(board_size_option2_int)
board_size_option3_text = str(board_size_option3_int) + "x" + str(board_size_option3_int)


# Defining ship options:
ship_option1 = "2, 3, 4, 5"
ship_option2 = "2, 2, 3, 3"
ship_option3 = "2, 6"

main_menu_window = tkinter.Tk()
main_menu_window.title("Battleships")
main_menu_window.resizable(False, False)
main_menu_window.configure(padx=10, pady=10)

tkinter.Label(main_menu_window, text="BATTLESHIPS GAME", font=("Castellar", 18), anchor='center', pady=10, padx=70)\
    .grid(row=0, column=0, columnspan=8, sticky='ew')

# Creating Difficulty level label
tkinter.Label(main_menu_window, text="Difficulty level", font=("Arial Bold", 10)).grid(row=1, column=0, columnspan=3, sticky='w')
# Creating a value for the Difficulty level radio buttons and setting "Easy" as the default:
difficulty_level = tkinter.Variable(value="Easy")
# Creating Difficulty level radio buttons:
tkinter.Radiobutton(main_menu_window, text="Easy", variable=difficulty_level, value="Easy")\
    .grid(row=2, column=0, columnspan=2, sticky='w')
tkinter.Radiobutton(main_menu_window, text="Hard", variable=difficulty_level, value="Hard")\
    .grid(row=3, column=0, columnspan=2, sticky='w')

# Creating Board size label:
tkinter.Label(main_menu_window, text="Board size", font=("Arial Bold", 10)).grid(row=1, column=3, columnspan=3, sticky='w')
# Creating a value for the Board size radio buttons and setting 8x8 as the default:
board_size = tkinter.IntVar(value=board_size_option1_int)
# Creating Board size radio buttons:
tkinter.Radiobutton(main_menu_window, text=board_size_option1_text, variable=board_size, value=board_size_option1_int) \
    .grid(row=2, column=3, columnspan=3, sticky='w')
tkinter.Radiobutton(main_menu_window, text=board_size_option2_text, variable=board_size, value=board_size_option2_int) \
    .grid(row=3, column=3, columnspan=3, sticky='w')
tkinter.Radiobutton(main_menu_window, text=board_size_option3_text, variable=board_size, value=board_size_option3_int) \
    .grid(row=4, column=3, columnspan=3, sticky='w')

# Creating Ship configuration label:
tkinter.Label(main_menu_window, text="Ship configuration", font=("Arial Bold", 10)).grid(row=1, column=6, columnspan=3, sticky='w')
# Creating a value for the Ship configuration radio buttons and setting 2,3,4,5 as the default:
ship_lengths = tkinter.Variable(value=ship_option1)
# Creating Ship configuration radio buttons:
tkinter.Radiobutton(main_menu_window, text=ship_option1, variable=ship_lengths, value=ship_option1) \
    .grid(row=2, column=6, columnspan=2, sticky='w')
tkinter.Radiobutton(main_menu_window, text=ship_option2, variable=ship_lengths, value=ship_option2) \
    .grid(row=3, column=6, columnspan=2, sticky='w')
tkinter.Radiobutton(main_menu_window, text=ship_option3, variable=ship_lengths, value=ship_option3) \
    .grid(row=4, column=6, columnspan=2, sticky='w')

# Creating a separate frame for the Start and Quit buttons.
# This is needed to be able to align them easily.
buttons_frame = tkinter.Frame(main_menu_window)
buttons_frame.grid(row=6, column=0, columnspan=9)

# Setting row size, to leave gap between radio buttons and start / quit buttons.
buttons_frame.rowconfigure(0, minsize=60)

# Start button. Setting required width, and padding:
button_start = tkinter.Button(
    buttons_frame,
    text="Start",
    command=lambda: run_ship_placement(difficulty_level.get(), board_size.get(), ship_lengths.get()),
    width=14
)
button_start.grid(row=0, column=0, padx=30, pady=5, sticky='s')

# Quit button. Setting required width, and padding:
button_quit = tkinter.Button(buttons_frame, text="Quit", command=main_menu_window.destroy, width=14)
button_quit.grid(row=0, column=1, padx=30, pady=5, sticky='s')

main_menu_window.mainloop()
