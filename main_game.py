import ship_setup
from ship_setup import HORIZONTAL, VERTICAL
import btn
import ship
import board
import json
import random

# TODO protect variable by adding _ at the start
# TODO add validation checks for all variables

# comp_ship1 = ship.Ship(start_row=3, start_column=ship_setup.board_size+4, orientation="horizontal", length=2)
# comp_ship2 = ship.Ship(start_row=1, start_column=ship_setup.board_size+2, orientation="vertical", length=4)
# comp_ship3 = ship.Ship(start_row=5, start_column=ship_setup.board_size+6, orientation="horizontal", length=2)
#
ships = {"human": [], "computer": []}


if ship_setup.field_location_computer == "left":
    first_column = 0
else:
    first_column = ship_setup.board_size + 1

# Creating dicts storing all available coordinates.
# The available coordinates for each ship would depend on its orientation
# hence the two separate lists. They need to be lists instead of sets,
# to pass to the random.choice() function:

available_coordinates = {
    HORIZONTAL: [(row, col) for row in range(ship_setup.board_size) for col in
                 range(first_column, ship_setup.board_size + first_column)],
    VERTICAL: [(row, col) for row in range(ship_setup.board_size) for col in
               range(first_column, ship_setup.board_size + first_column)],
}

taken_coordinates = []

for length in ship_setup.ship_configuration:
    orientation = random.randint(HORIZONTAL, VERTICAL)
    coordinates = available_coordinates[orientation].copy()     # Must be a copy, otherwise it's the same list
    if orientation == HORIZONTAL:
        for coordinate in coordinates[::-1]:
            # Must go backwards, so that deleting items would not mess with the loop variable
            if coordinate[1] > (ship_setup.board_size - length + first_column):
                coordinates.remove(coordinate)
            else:
                # Removing all potential clash coordinates with other ships
                for taken_coordinate in taken_coordinates:
                    # if in the given row there is already a ship, remove all clash coordinates
                    if taken_coordinate[0] == coordinate[0] and \
                            (coordinate[1] + length > taken_coordinate[1] >= coordinate[1]):
                        coordinates.remove(coordinate)
                        break  # break once coordinate is removed
    else:
        for coordinate in coordinates[::-1]:
            if coordinate[0] > (ship_setup.board_size - length):
                coordinates.remove(coordinate)
            else:
                # Removing all potential clash coordinates with other ships
                for taken_coordinate in taken_coordinates:
                    # if in the given column there is already a ship, remove all clash coordinates
                    if taken_coordinate[1] == coordinate[1] and \
                            (coordinate[0] + length > taken_coordinate[0] >= coordinate[0]):
                        coordinates.remove(coordinate)
                        break   # break once coordinate is removed
    print(coordinates)
    random_coordinate = random.choice(coordinates)
    new_ship = ship.Ship(start_row=random_coordinate[0],
                         start_column=random_coordinate[1],
                         orientation=orientation, length=length)
    if orientation == HORIZONTAL:
        for i in range(length):
            taken_coordinates.append((random_coordinate[0], random_coordinate[1]+i))
    else:
        for i in range(length):
            taken_coordinates.append((random_coordinate[0]+i, random_coordinate[1]))
    print(taken_coordinates)
    available_coordinates[HORIZONTAL].remove(random_coordinate)
    available_coordinates[VERTICAL].remove(random_coordinate)
    ships["computer"].append(new_ship)

with open("ships_config.json", encoding="utf-8") as ships_config:
    ships_settings = json.load(ships_config)

for item in ships_settings:
    new_ship = ship.Ship(start_row=item["start row"], start_column=item["start column"],
                         orientation=item["orientation"], length=item["length"])
    ships["human"].append(new_ship)

human_board = board.GameBoard(size=ship_setup.board_size, window=ship_setup.mainWindow,
                              button_class=btn.Btn, ships_list=ships["human"], player="human")
human_board.draw_game_field(ship_setup.field_location_human)

computer_board = board.GameBoard(size=ship_setup.board_size, window=ship_setup.mainWindow,
                                 button_class=btn.Btn, opponent=human_board, ships_list=ships["computer"], player="computer")
computer_board.draw_game_field(ship_setup.field_location_computer)

# for testing:
for i in ships["computer"]:
    print(f"row: {i.start_row}, column: {i.start_column}, orientation: {i.orientation}, length: {i.length}")
print()
# for testing:
for i in ships["human"]:
    print(f"row: {i.start_row}, column: {i.start_column}, orientation: {i.orientation}, length: {i.length}")

ship_setup.mainWindow.mainloop()
