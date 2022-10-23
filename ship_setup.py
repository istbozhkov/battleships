import tkinter
import json

HORIZONTAL = 0
VERTICAL = 1

mainWindow = tkinter.Tk()

mainWindow.title("Battleships")
mainWindow.resizable(False, False)

with open("config.json", encoding="utf-8") as config:
    settings = json.load(config)

board_size = settings["board size"]
ship_configuration = settings["ship configuration"]
difficulty_level = settings["difficulty level"]
field_location_human = "left"   # location of the human board - i.e. where the computer is attacking
field_location_computer = "right"   # location of the computer board - i.e. where the human is attacking
