# -*- coding: utf-8 -*-

import numpy as np
from gamestate import GameState
from local_db import DB
import array_comparison as ac
from abc import ABC, abstractmethod


def get_possible_states(previous_gamestate):
    """Yields all possible unique states that follow from given previous
    gamestate."""
    next_to_move = previous_gamestate.next_to_move()
    indexes = np.nonzero(previous_gamestate.state == "-")

    def move_generator():
        for i in range(len(indexes[0])):
            ndarr = np.copy(previous_gamestate.state)
            ndarr[indexes[0][i], indexes[1][i]] = next_to_move
            yield ndarr

    gamestates = []
    for arr in move_generator():
        for gs in gamestates:
            if ac.are_sqr_arrays_equal(gs, arr):
                continue
        gamestates.append(arr)
        yield GameState(arr)


class AI(ABC):
    @abstractmethod
    def get_next_gamestate(self, previous_gamestate):
        pass

    @abstractmethod
    def update_db(self, gamestates):
        pass


class WeightedGameStateAI(AI):
    """Machine learning AI that uses weights to select game states."""
    def __init__(self, update_database=True):
        self.db = DB()
        self.update_database = update_database

    def get_next_gamestate(self, previous_gamestate):
        """Returns next game state based on the previous state."""
        # Check if game has ended either in victory or draw
        ended, message = previous_gamestate.is_game_over()
        if ended:
            return {
                "outcome": message
            }

        # Check if possible states are in the database and randomize
        # the weight a bit.
        def move_randomizer():
            for gs in get_possible_states(previous_gamestate):
                weight = self.db.get_weight(gs)
                randomized_weight = np.random.normal(loc=1.0, scale=0.1) * weight.weight
                yield {
                    "state": gs,
                    "randomized_weight": randomized_weight
                }

        # 'X' player tries to find the state with maximum weight while
        # 'O' player goes for the state with lowest weight.
        if previous_gamestate.next_to_move() == "X":
            next_move = max(
                move_randomizer(), key=lambda x: x["randomized_weight"])
        else:
            next_move = min(
                move_randomizer(), key=lambda x: x["randomized_weight"])

        # If it's the first turn, randomly rotate the state
        selected_state = next_move["state"]
        if previous_gamestate.rounds_played == 0:
            selected_state.rotate(np.random.randint(0, high=3))

        return selected_state

    def update_db(self, gamestates):
        if self.update_database:
            is_game_over, message = gamestates[-1].is_game_over()

            for gamestate in gamestates:
                self.db.add_or_update(gamestate, message)


class RandomAI(AI):
    def get_next_gamestate(self, previous_gamestate):
        return np.random.choice(
            list(get_possible_states(previous_gamestate)), size=1)[0]

    def update_db(self, gamestates):
        pass
