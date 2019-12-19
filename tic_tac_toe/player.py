# -*- coding: utf-8 -*-

from gamestate import GameState


class Player(object):
    def __init__(self, name, ai=None):
        self.name = name
        self.ai = ai

    def get_next_gamestate(self, previous_gamestate):
        if self.ai:
            return self.ai.get_next_gamestate(previous_gamestate)
        else:
            raise NotImplementedError("Human player not yet implemented")
