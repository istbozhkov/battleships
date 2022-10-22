import random
import tkinter
import json
import ship_setup
from ship_setup import HORIZONTAL, VERTICAL


class Board:
    def __init__(self, size, window, button_class, player=None):     # TODO add function annotations
        self.size = size
        self.window = window
        self.player = player    # governs whether the board will be operated by a person or by the computer

        self.button_class = button_class
        self.button = None
        self.message_text = tkinter.StringVar()
        self.message_field = None
        self.game_field = None

    def draw_field(self, button_function, start_cell):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]

        self.game_field = tkinter.Frame(self.window)
        self.game_field.grid(row=1, column=start_cell+1, rowspan=self.size, columnspan=self.size, padx=5)

        # Coordinate labels
        for column in range(start_cell, self.size + start_cell):
            tkinter.Label(self.game_field, text=letters[column-start_cell], font='bold', height=2, anchor='s') \
                .grid(sticky="ew", row=0, column=column + 1)
        for row in range(self.size):
            tkinter.Label(self.game_field, text=row+1, font='bold', width=3, anchor='e') \
                .grid(column=start_cell, row=row + 1)

        # Creating field buttons.
        # button_image = tkinter.PhotoImage(file="sea_pattern.png")
        for column in range(start_cell, self.size + start_cell):
            for row in range(self.size):
                self.button = self.button_class(self.game_field)
                self.button.default_button(row, column)
                if self.player != "human":  # if it's the computer's board, the buttons are clickable.
                    self.button.configure(command=lambda btn_row=row, btn_column=column: button_function(btn_row, btn_column))
                else:
                    self.button["state"] = "disabled"

    def draw_message_field(self, initial_message, start_cell):
        self.message_text.set(initial_message)
        border_color = tkinter.Frame(self.window, background="green")
        border_color.grid(row=self.size + 1, column=1+start_cell, padx=25, pady=5)
        self.message_field = tkinter.Label(border_color, textvariable=self.message_text,
                                           font=("Lucida Sans Typewriter", 9, "bold"), bg="black", fg="green",
                                           anchor="w", width=40, bd=0)
        self.message_field.pack(padx=1, pady=1)


class SetUpBoard(Board):
    def __init__(self, ship_configuration, size, window, button_class, player=None):
        super().__init__(size=size, window=window, button_class=button_class, player=player)
        # for ship placement only:
        self.ship_configuration = ship_configuration
        self.ship_qty = 0
        self.ship_size = 0
        self.ship_orientation = ""
        self.ship_data = []
        self.latest_rb = None
        self.button_start = None    # Needed to be global so that it can be updated when placing the last ship.
        self.placed_ships_coordinates = set()   # creating an empty set for the placed ships coordinates
        # TODO could pass them to the Ship class later if needed (as they are calculated again there)
        self.ship_configuration_list = []   # needed to pass to ship_config.json

    def draw_placement_field(self, run_function):
        self.ship_qty = len(self.ship_configuration)  # Must be initialized here, in case the Clear button is pressed.
        self.ship_configuration_list = []   # Zeroing here in case the Clear button is pressed.
        self.placed_ships_coordinates = set()   # Zeroing here in case the Clear button is pressed.
        start_cell = 0  # Only showing human player's board, so start cell is always 0

        super().draw_field(button_function=self.place_ship, start_cell=start_cell)
        super().draw_message_field(initial_message="Choose a coordinate to place a ship...", start_cell=start_cell)

        # ---- The remainder of this function sets up the settings field:

        settings_field = tkinter.Frame(self.window)
        settings_field.grid(row=2, column=(self.size * 2) + 3, padx=5)

        tkinter.Label(settings_field, text="Select a ship to place", font=("Arial Bold", 10)) \
            .grid(row=0, column=0, columnspan=2, sticky='w')
        self.ship_size = tkinter.IntVar(value=self.ship_configuration[0])
        # TODO: once we have the settings from the main_menu, pass the ship size variable to `text` and `value` below
        rb1 = tkinter.Radiobutton(settings_field, text="Length " + str(self.ship_configuration[0]),
                                  variable=self.ship_size, value=self.ship_configuration[0],
                                  command=lambda: rb_change("rb1"))
        rb1.grid(row=1, column=0, columnspan=2, sticky='w')
        # Adding +0.1 (or 0.2/3) to the value so that in case there are more than one ships with the same length,
        # The radio button will still show the correct selection.
        # The float will be converted to integer by the IntVar, so it will cause no issues with the functionality.
        # TODO: save this example as a clever solution.
        rb2 = tkinter.Radiobutton(settings_field, text="Length " + str(self.ship_configuration[1]),
                                  variable=self.ship_size, value=self.ship_configuration[1]+0.1,
                                  command=lambda: rb_change("rb2"))
        rb2.grid(row=2, column=0, columnspan=2, sticky='w')
        if self.ship_qty > 2:
            rb3 = tkinter.Radiobutton(settings_field, text="Length " + str(self.ship_configuration[2]),
                                      variable=self.ship_size, value=self.ship_configuration[2]+0.2,
                                      command=lambda: rb_change("rb3"))
            rb3.grid(row=3, column=0, columnspan=2, sticky='w')
        if self.ship_qty > 3:
            rb4 = tkinter.Radiobutton(settings_field, text="Length " + str(self.ship_configuration[3]),
                                      variable=self.ship_size, value=self.ship_configuration[3]+0.3,
                                      command=lambda: rb_change("rb4"))
            rb4.grid(row=4, column=0, columnspan=2, sticky='w')
        if self.ship_qty > 4:
            raise ValueError("More ships than expected!")

        self.latest_rb = rb1    # setting default value for latest_rb (in case ship is placed, without changing the rb)

        def rb_change(rb):
            # When a RB is changed, it is saved in an attribute, so that it can be disabled if a ship is placed
            # TODO change this to a docstring
            if rb == "rb1":
                self.latest_rb = rb1
            elif rb == "rb2":
                self.latest_rb = rb2
            elif rb == "rb3":
                self.latest_rb = rb3
            else:
                self.latest_rb = rb4
            self.message_text.set("Choose a coordinate to place a ship...")

        # Ship orientation radio buttons and label:
        tkinter.Label(settings_field, text="Select ship orientation", font=("Arial Bold", 10), anchor='s', height=2) \
            .grid(row=5, column=0, columnspan=2, sticky='w')
        self.ship_orientation = tkinter.Variable(value=HORIZONTAL)
        tkinter.Radiobutton(settings_field, text="Horizontal", variable=self.ship_orientation, value=HORIZONTAL) \
            .grid(row=6, column=0, columnspan=2, sticky='w')
        tkinter.Radiobutton(settings_field, text="Vertical", variable=self.ship_orientation, value=VERTICAL) \
            .grid(row=7, column=0, columnspan=2, sticky='w')

        button_clear = tkinter.Button(settings_field, text="Clear", width=15,
                                      command=lambda: self.draw_placement_field(run_function))
        button_clear.grid(row=8, column=0, padx=30, pady=30, sticky='s')

        self.button_start = tkinter.Button(settings_field, text="Start", width=15, command=run_function)
        self.button_start.grid(row=9, column=0, padx=30, sticky='s')
        self.button_start["state"] = "disabled"

    def place_ship(self, row, column):
        is_placed = False
        if self.latest_rb["state"] == "disabled":   # Checking whether user has chosen a new ship to place.
            self.message_text.set("Choose another ship to place")
        else:
            # Checking if ship can be placed entirely within field boundaries:
            if (self.ship_orientation.get() == HORIZONTAL and (self.size - column) >= self.ship_size.get()) or \
                    (self.ship_orientation.get() == VERTICAL and (self.size - row) >= self.ship_size.get()):
                self.ship_data.append((row, column, self.ship_orientation.get(), self.ship_size.get()))

                # Displaying placed ship:
                if self.ship_orientation.get() == HORIZONTAL:
                    for i in range(self.ship_size.get()):
                        # Checking to see if there is a ship in the way
                        if (row, column+i) in self.placed_ships_coordinates:
                            # A ship is in the way -> breaking the loop, so the else statement won't get executed.
                            self.message_text.set("There is another ship in the way!")
                            break
                    else:
                        for i in range(self.ship_size.get()):
                            if i == 0:
                                picture = "front"
                            elif i == self.ship_size.get()-1:
                                picture = "rear"
                            else:
                                picture = "mid"
                            picture += str(self.ship_orientation.get())
                            self.button = self.button_class(self.game_field)
                            self.button.ship_display(row=row, column=column+i, picture=picture)
                            self.button["state"] = "disabled"
                            # adding placed ship coordinates:
                            self.placed_ships_coordinates.add((row, column+i))
                        is_placed = True

                else:  # if vertical
                    for i in range(self.ship_size.get()):
                        # Checking to see if there is a ship in the way
                        if (row+i, column) in self.placed_ships_coordinates:
                            # A ship has been placed -> breaking the loop, so the else statement won't get executed.
                            self.message_text.set("There is another ship in the way!")
                            break
                    else:
                        # adding placed ship column to "taken" coordinates:
                        for i in range(self.ship_size.get()):
                            if i == 0:
                                picture = "front"
                            elif i == self.ship_size.get()-1:
                                picture = "rear"
                            else:
                                picture = "mid"
                            picture += str(self.ship_orientation.get())
                            self.button = self.button_class(self.game_field)
                            self.button.ship_display(row=row+i, column=column, picture=picture)
                            self.button["state"] = "disabled"
                            # adding placed ship coordinates:
                            self.placed_ships_coordinates.add((row+i, column))
                        is_placed = True
            else:
                self.message_text.set("Ship must be entirely within the field!")

        if is_placed:
            self.latest_rb["state"] = "disabled"
            self.ship_qty -= 1  # Removing one from the remaining ships to be placed
            self.ship_configuration_list.append({
                "start row": row,
                "start column": column,
                "orientation": self.ship_orientation.get(),
                "length": self.ship_size.get()
            })
            with open("ships_config.json", "w", encoding="utf-8") as ships_file:
                json.dump(self.ship_configuration_list, ships_file)

            if self.ship_qty:
                self.message_text.set("Choose another ship to place")
            else:
                # if all ships are already placed
                self.message_text.set("Press Start to start the game")

        if self.ship_qty == 0:
            self.button_start["state"] = "active"


class GameBoard(Board):
    def __init__(self, size, window, ships_list: list, button_class, opponent=None, player="human"):
        super().__init__(size=size, window=window, button_class=button_class, player=player)
        self.opponent = opponent    # opponent's Board instance.
        # Only needed for computer's board, so that the computer can call the human board's shoot method
        self.ships = ships_list
        self.available_coordinates = []
        self.hit_target = False  # Used in Difficult Mode algorithm
        self.last_shot = ()  # Used in Difficult Mode algorithm

    def draw_game_field(self, location):

        # Creating a list of the available coordinates for the computer to shoot at.
        # Note that the computer shoots at the human's board and vice versa.
        if self.player == "computer":
            for row in range(self.size):
                if location == "right":
                    for column in range(self.size):
                        self.available_coordinates.append((row, column))
                else:
                    for column in range(self.size + 1, (2 * self.size) + 1):
                        self.available_coordinates.append((row, column))  # TODO Check that this works properly

        if location == "left":
            start_cell = 0
        else:
            start_cell = self.size + 1

        super().draw_field(button_function=self.shoot, start_cell=start_cell)

        if self.player == "human":  # displaying the human's ships on their board
            for vessel in self.ships:   # Named `vessel` instead of `ship` to avoid confusion with the Ship class
                for coordinate in vessel.coordinates:
                    print(vessel.start_row)
                    print(vessel.length)
                    print(f"coordinate: {coordinate[0]}")
                    if coordinate == (vessel.start_row, vessel.start_column):
                        picture = "front"
                    elif coordinate[0] == vessel.length + vessel.start_row - 1 or\
                            coordinate[1] == vessel.length + vessel.start_column - 1:
                        picture = "rear"
                    else:
                        picture = "mid"
                    picture += str(vessel.orientation)
                    self.button = self.button_class(self.game_field)
                    self.button.ship_display(row=coordinate[0], column=coordinate[1], picture=picture)
                    self.button["state"] = "disabled"
        else:   # showing message field under computer's board:
            super().draw_message_field(initial_message="Choose a coordinate to shoot at...", start_cell=start_cell)

    def already_shot(self):
        #   Displays a relevant message if user shoots twice at the same coordinates.
        self.message_text.set("Already shot at these coordinates!")
        if self.player == "human":
            self.button["state"] = "disabled"

    def shoot(self, row, column):
        # Checking if a ship is hit.
        for vessel in self.ships:   # Named `vessel` instead of `ship` to avoid confusion with the Ship class
            if vessel.is_hit(row, column):
                self.button = self.button_class(self.game_field)
                self.button.hit_target(row, column)
                self.button.configure(command=self.already_shot)
                self.hit_target = True  # Used in Difficult Mode algorithm
                self.message_text.set(f"Remaining ships: {len(self.ships)}")
                if vessel.is_sunk:
                    self.ships.remove(vessel)  # removing the ship from the list of ship.
                    # This will make it easier to check further hits
                    # and make it immediately obvious when the player / computer has lost.
                    self.message_text.set(f"Remaining ships: {len(self.ships)}")
                    if len(self.ships) == 0:
                        self.message_text.set("You won!")
                        break
                break
        else:
            self.button = self.button_class(self.game_field)
            self.button.miss_target(row, column)
            self.button.configure(command=self.already_shot)
            self.message_text.set(f"Remaining ships: {len(self.ships)}")
            self.hit_target = False

        if self.player == "human":
            self.button["state"] = "disabled"   # disabling the buttons of the human board
        else:
            # Computer shoot method called at the end of every human turn.
            def shoot_random():
                rand_row, rand_col = random.choice(self.available_coordinates)
                self.opponent.shoot(rand_row, rand_col)
                self.available_coordinates.remove((rand_row, rand_col))
                # removing shoot coordinates from list of available coordinates
                self.opponent.last_shot = (rand_row, rand_col)  # Only needed for Difficult Mode
            if ship_setup.difficulty_level == "Easy":
                # Easy mode - shoot at random
                shoot_random()
            else:
                # Difficult mode - if a hit is ship - shoot next to it
                if not self.opponent.hit_target:
                    # If no ship was hit - shoot at random.
                    shoot_random()
                else:
                    last_row, last_column = self.opponent.last_shot
                    adjacent_coordinates = [(last_row, last_column + 1), (last_row, last_column - 1),
                                            (last_row - 1, last_column), (last_row + 1, last_column)]
                    # Converting to set for more efficient search:
                    available_coordinates_set = set(self.available_coordinates)
                    for coordinate in adjacent_coordinates:
                        if coordinate in available_coordinates_set:
                            self.opponent.shoot(*coordinate)
                            self.available_coordinates.remove(coordinate)
                            if self.opponent.hit_target:
                                # Saving coordinates only if ship's been hit
                                # Otherwise want to keep shooting around previous hit
                                self.opponent.last_shot = coordinate
                            else:
                                # Changing back to True, so that it can continue shooting original adjacent coords.
                                self.opponent.hit_target = True
                            break
                    else:
                        shoot_random()  # if none of the adjacent coordinates is available -> shoot at random

