# -*- coding: utf-8 -*-

import array_comparison as ac
from gamestate import GameState


_weight_adjustements = {
    "X won!": 1.0,
    "O won!": 0.0,
    "Draw.": 0.7
}


class Weight:
    def __init__(self, weigth=0.7, playcount=0):
        self.weight = weigth
        self.playcount = playcount


class DB:
    """Database contains all unique gamestates that the AI has encountered
    as well as their weights and play counts.

    TODO serialize this to file."""
    def __init__(self, default_weight=0.7):
        self.rounds = {
            0: {},
            1: {},
            2: {},
            3: {},
            4: {},
            5: {},
            6: {},
            7: {},
            8: {},
            9: {}
        }
        self.default_weight = default_weight

    def add_or_update(self, gamestate, result):
        """If the gamestate is already in the database, its values
        will be updated, otherwise the state is added to the
        database."""
        weight = self.get_weight(gamestate)
        if weight.playcount == 0:
            self.rounds[gamestate.rounds_played][gamestate] = weight

        weight_adjustment = _weight_adjustements[result]

        weight.playcount += 1
        weight.weight = ((weight.playcount * weight.weight) + weight_adjustment) / (weight.playcount + 1)

    def get_weighted_states(self, rounds=[]):
        """Returns all known states for given rounds."""
        res = []
        for r in rounds:
            res += self.rounds[r]
        return res

    def get_weight(self, gamestate):
        """Returns weight that corresponds to the given gamestate.

        If gamestate is not in database, default value is returned."""
        if gamestate in self.rounds[gamestate.rounds_played]:
            return self.rounds[gamestate.rounds_played][gamestate]
        return Weight()
