# -*- coding: utf-8 -*-

from gamestate import GameState
from player import Player
from AI import WeightedGameStateAI, RandomAI
from itertools import permutations
import time
from typing import Iterable
from math import factorial


class TicTacToe:
    def __init__(self, time_between_moves=0, print_moves=False):
        self.time_between_moves = time_between_moves
        self.print_moves = print_moves

    def play_game(self, x_player: Player, o_player: Player):
        current_gamestate = GameState()
        gamestate_history = []
        players = {
            "X": x_player,
            "O": o_player
        }

        while True:
            gamestate_history.append(current_gamestate)
            if self.print_moves:
                print(current_gamestate)
            is_game_over, msg = current_gamestate.is_game_over()
            if is_game_over:
                break
            next_player = players[current_gamestate.next_to_move()]
            current_gamestate = next_player.get_next_gamestate(
                current_gamestate
            )
            time.sleep(self.time_between_moves)

        if x_player.ai:
            x_player.ai.update_db(gamestate_history)
        if o_player.ai:
            o_player.ai.update_db(gamestate_history)

        return msg

    def play_tournament(self, rounds: int, players: Iterable[Player]):
        """Plays a round robin tournament between all players.

        All players will play both as 'X' and as 'O' against all the 
        other players for given number of rounds."""
        results = dict([
            (p.name, {
                "wins": 0,
                "draws": 0,
                "losses": 0
            }) for p in players
        ])
        for p in players:
            results[p.name] = {
                "wins": 0,
                "draws": 0,
                "losses": 0
            }

        print_interval = _get_print_interval(rounds, len(players), 50)
        print("Running a tournament. Total number of matches to be played {0}.".format(
            _get_match_count(rounds, len(players))
        ))

        for p1, p2 in permutations(players, 2):
            i = 0
            for j in range(rounds):
                if (i * rounds + j) % print_interval == 0:
                    print(".", end="") 
                res = self.play_game(p1, p2)
                if res == "X won!":
                    results[p1.name]["wins"] += 1
                    results[p2.name]["losses"] += 1
                elif res == "O won!":
                    results[p1.name]["losses"] += 1
                    results[p2.name]["wins"] += 1
                else:
                    results[p1.name]["draws"] += 1
                    results[p2.name]["draws"] += 1
            i += 1

        print("\nTournament finished")
        return results


def _get_match_count(round_count, player_count):
    if player_count < 2 or round_count < 1:
        return 0
    permutation_count = int(
        factorial(player_count / factorial(player_count - 2)))
    return round_count * permutation_count


def _get_print_interval(round_count, player_count, print_count):
    interval = int(_get_match_count(
        round_count, player_count) / print_count)
    return interval if interval != 0 else 1


if __name__ == "__main__":
    game = TicTacToe()

    from timeit import default_timer as timer

    p1 = Player("player1", WeightedGameStateAI())
    p2 = Player("player2", WeightedGameStateAI())
    p3 = Player("player3", RandomAI())

    start = timer()
    # Training round
    game.play_tournament(50, [p1, p2, p3])
    stop = timer()
    print("Training finished in {0} seconds.".format(stop - start))

    start = timer()
    # Actual tournament
    res = game.play_tournament(10, [p1, p2, p3])
    stop = timer()
    print("Tournament finished in {0} seconds.".format(stop - start))
    print("Results:\n{0}".format(res))
