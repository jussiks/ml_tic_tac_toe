import unittest
import array_comparison as ac
from gamestate import GameState
import numpy as np


class TestArrayComparison(unittest.TestCase):
    def test_generate_equal_arrays(self):
        self.assertRaises(
            ValueError, lambda: list(ac.generate_equal_arrays("XOXOXOXOX")))
        self.assertRaises(
            ValueError, lambda: list(ac.generate_equal_arrays([])))
        self.assertRaises(
            ValueError, lambda: list(ac.generate_equal_arrays([[]])))
        self.assertEqual(
            [np.array([1]) for i in range(8)],
            list(ac.generate_equal_arrays([[1]]))
            )

        expected = [
            np.array([[1, 3], [0, 2]]),
            np.array([[3, 2], [1, 0]]),
            np.array([[2, 0], [3, 1]]),
            np.array([[0, 1], [2, 3]]),
            np.array([[0, 2], [1, 3]]),
            np.array([[2, 3], [0, 1]]),
            np.array([[3, 1], [2, 0]]),
            np.array([[1, 0], [3, 2]])
            ]
        actual = ac.generate_equal_arrays([[0, 1], [2, 3]])

        for e, a in zip(expected, actual):
            self.assertTrue(np.array_equal(e, a),
                            msg="{0} does not equal {1}.".format(e, a))

    def test_are_sqr_arrays_equal(self):
        x = [
            ["X", "-", "X"],
            ["O", "X", "-"],
            ["O", "-", "-"]
        ]
        x_rotated = [
            ["X", "-", "-"],
            ["-", "X", "-"],
            ["X", "O", "O"]
        ]
        x_mirrored = [
            ["X", "-", "X"],
            ["-", "X", "O"],
            ["-", "-", "O"]
        ]
        x_rot_mir = [
            ["-", "-", "X"],
            ["-", "X", "-"],
            ["O", "O", "X"]
        ]
        x_partial_rotation = [
            ["-", "X", "-"],
            ["X", "X", "-"],
            ["O", "O", "-"]
        ]
        x_partial_mirror = [
            ["X", "-", "X"],
            ["O", "X", "-"],
            ["-", "-", "O"]
        ]
        self.assertTrue(ac.are_sqr_arrays_equal(x, x_rotated))
        self.assertTrue(ac.are_sqr_arrays_equal(x, x_mirrored))
        self.assertTrue(ac.are_sqr_arrays_equal(x, x_rot_mir))
        self.assertFalse(ac.are_sqr_arrays_equal(x, x_partial_rotation))
        self.assertFalse(ac.are_sqr_arrays_equal(x, x_partial_mirror))


class TestGameState(unittest.TestCase):
    def test_gamestate(self):
        self.assertRaises(
            ValueError, lambda: GameState([]))
        self.assertRaises(
            ValueError, lambda: GameState([
                ["X", "-", "-"],
                ["-", "-", "-"],
                ["-", "-"]]))
        self.assertRaises(
            ValueError, lambda: GameState([
                ["X", "-", "-"],
                ["-", "-", "-"],
                ["-", "-", "X"]]))
        gs1 = GameState([
                ["X", "-", "-"],
                ["-", "-", "-"],
                ["-", "-", "O"]]
            )
        self.assertEqual(2, gs1.rounds_played)
        self.assertEqual("X", gs1.next_to_move())
        gs2 = GameState([
                ["O", "-", "-"],
                ["-", "-", "-"],
                ["-", "-", "X"]]
            )
        self.assertEqual(gs1, gs2)
        self.assertEqual(hash(gs1), hash(gs2))
        b, m = gs2.is_game_over()
        self.assertFalse(b)

        gs3 = GameState([
            ["X", "X", "X"],
            ["O", "O", "-"],
            ["-", "-", "-"]
        ])

        self.assertNotEqual(gs1, gs3)
        b, m = gs3.is_game_over()
        self.assertTrue(b)
        self.assertEqual(m, "X won!")


if __name__ == "__main__":
    unittest.main()
