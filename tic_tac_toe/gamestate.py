# -*- coding: utf-8 -*-

import numpy as np
import array_comparison as ac


# Initial empty gamestate
_initial_gamestate = [
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"]
]


class GameState(object):
    def __init__(self, array=None):
        array = array if array is not None else _initial_gamestate
        self.state = np.array(array)
        try:
            self.char_counts = self.count_chars()
        except TypeError as e:
            raise ValueError("Not a valid game state: " + str(e))
        self.rounds_played = self.get_rounds_played()
        self.is_valid, message = self.is_state_valid()
        if not self.is_valid:
            raise ValueError("Not a valid game state: " + message)

    def __eq__(self, other_gamestate):
        if not isinstance(other_gamestate, GameState):
            return NotImplemented

        return ac.are_sqr_arrays_equal(self.state, other_gamestate.state)

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        arr = [str(a) for a in ac.generate_equal_arrays(self.state)]
        arr.sort()
        return hash("".join(arr))

    def is_state_valid(self):
        if not self.state.shape == (3, 3):
            return False, "State is not an 3X3 square."

        # Count number of X's, O's and -'s
        if self.char_counts["X"] + self.char_counts["O"] + self.char_counts["-"] != 9:
            return False, "Wrong number of characters."

        if self.char_counts["O"] > self.char_counts["X"]:
            return False, "Too many O's"

        if self.char_counts["O"] + 1 < self.char_counts["X"]:
            return False, "Too may X's"

        # TODO check that no two winning lines exist

        return True, "State is valid"

    def is_game_over(self):
        # Row check
        for row in self.state:
            if "-" != row[0] == row[1] == row[2]:
                return True, "{0} won!".format(row[0])

        # Column check
        for column in self.state.T:
            if "-" != column[0] == column[1] == column[2]:
                return True, "{0} won!".format(column[0])

        # Diagonal checks
        diag = np.diag(self.state)
        if "-" != diag[0] == diag[1] == diag[2]:
            return True, "{0} won!".format(diag[0])

        diag = np.diag(np.rot90(self.state))
        if "-" != diag[0] == diag[1] == diag[2]:
            return True, "{0} won!".format(diag[0])

        if self.char_counts["-"] == 0:
            return True, "Draw."

        return False, "Game continues"

    def count_chars(self):
        unique, counts = np.unique(self.state, return_counts=True)
        counts_dict = dict(zip(unique, counts))

        if "X" not in counts_dict:
            counts_dict["X"] = 0
        if "O" not in counts_dict:
            counts_dict["O"] = 0
        if "-" not in counts_dict:
            counts_dict["-"] = 0

        return counts_dict

    def get_rounds_played(self):
        rounds = self.char_counts["O"] + self.char_counts["X"]
        if type(rounds) is np.int64:
            return rounds.item()
        return rounds

    def next_to_move(self):
        return "X" if self.rounds_played % 2 == 0 else "O"

    def rotate(self, turns):
        self.state = ac.rotate(self.state, turns=turns)
