from ship_setup import HORIZONTAL, VERTICAL


class Ship:
    def __init__(self, start_row, start_column, orientation, length):
        self.start_row = start_row  # row of top-left coordinate of the ship on the game board
        self.start_column = start_column  # column of top-left coordinate of the ship on the game board
        self.orientation = orientation  # HORIZONTAL or VERTICAL
        self.length = length    # number of `buttons` long
        self.coordinates = {(start_row, start_column)}  # initializing a set of tuples for the ship coordinates
        if self.orientation == HORIZONTAL:
            for i in range(self.length-1):  # running to length-1 because initial coordinates are already in the set
                self.coordinates.add((start_row, start_column+i+1))
        else:
            for i in range(self.length-1):  # running to length-1 because initial coordinates are already in the set
                self.coordinates.add((start_row+i+1, start_column))
        self.hits = set()   # initializing a set where all the hits will be stored for this ship
        self.is_sunk = False

    def is_hit(self, row, column):
        # check if there is a ship at the target coordinates
        if (row, column) in self.coordinates:
            self.hits.add((row, column))
            if self.hits == self.coordinates:
                self.is_sunk = True
            return True
        return False
