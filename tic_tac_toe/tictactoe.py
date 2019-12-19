# -*- coding: utf-8 -*-

from gamestate import GameState
from player import Player
from AI import WeightedGameStateAI, RandomAI
import time


class Game(object):
    def __init__(self, time_between_moves=1):
        self.ai1 = WeightedGameStateAI(update_database=True)
        self.ai2 = RandomAI()
        self.playerX = Player("player1", self.ai1)
        self.playerO = Player("player2", self.ai2)
        self.gamestates = []
        self.time_between_moves = time_between_moves

    def play(self):
        initial_gamestate = GameState()
        return self.add_move(initial_gamestate)

    def add_move(self, gamestate, print_state=False):
        time.sleep(self.time_between_moves)
        if print_state:
            print(gamestate)
        self.gamestates.append(gamestate)
        is_game_over, message = gamestate.is_game_over()
        if is_game_over:
            self.ai1.update_db(self.gamestates)
            self.ai2.update_db(self.gamestates)
            self.gamestates = []
            return message
        else:
            player_in_turn = self.playerX if gamestate.next_to_move() == "X" else self.playerO
            return self.add_move(player_in_turn.get_next_gamestate(gamestate))


if __name__ == "__main__":
    x_won = 0
    o_won = 0
    draws = 0

    game = Game(time_between_moves=0)

    from timeit import default_timer as timer

    start = timer()
    for i in range(1000):
        message = game.play()
        if message == "X won!":
            x_won += 1
        elif message == "O won!":
            o_won += 1
        else:
            draws += 1
        print("X: {0} Draws: {1} O: {2}".format(x_won, draws, o_won))
    stop = timer()
    print(stop - start)
