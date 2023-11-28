import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest
from battleship_spd.ai import (
    is_valid_ship_move,
    find_all_possible_ship_moves,
    find_best_move_hunt,
    find_splash_radius,
    find_best_move_target,
)


class TestAI(unittest.TestCase):
    def test_valid_ship_move(self):
        # Arrange
        board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        x_position = 1
        y_position = 1
        ship_length = 2
        is_vertical = True

        # Act
        result = is_valid_ship_move(
            board=board,
            x_position=x_position,
            y_position=y_position,
            ship_length=ship_length,
            is_vertical=is_vertical,
        )

        # Assert
        self.assertTrue(result)

    def test_invalid_ship_move(self):
        # Arrange
        board = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        x_position = 1
        y_position = 1
        ship_length = 3
        is_vertical = False

        # Act
        result = is_valid_ship_move(
            board=board,
            x_position=x_position,
            y_position=y_position,
            ship_length=ship_length,
            is_vertical=is_vertical,
        )

        # Assert
        self.assertFalse(result)

    def test_find_all_possible_ship_moves(self):
        # Arrange
        board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ship_length = 2

        # Act
        result = find_all_possible_ship_moves(board=board, ship_length=ship_length)

        # Assert
        expected_board = [[2, 3, 2], [3, 4, 3], [2, 3, 2]]
        self.assertTrue(result == expected_board)

    def test_find_best_move_hunt(self):
        # Arrange
        board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ship_lengths = [2]

        # Act
        _, result_x, result_y = find_best_move_hunt(
            board=board, ship_lengths=ship_lengths
        )

        # Assert
        expected_x = 1
        expected_y = 1

        self.assertTrue(expected_x == result_x)
        self.assertTrue(expected_y == result_y)

    def test_find_splash_radius(self):
        # Arrange
        board = [[0, 0, 0], [0, 0, 0], [0, 0, -2]]
        x_position = 2
        y_position = 2

        # Act
        result_board = find_splash_radius(board, x_position, y_position)

        # Assert
        expected_board = [[0, 0, 1], [0, 0, 2], [1, 2, -2]]
        self.assertTrue(result_board == expected_board)



    def test_find_best_move_target(self):
        # Arrange
        board = [[0, 0, 0], [0, 0, 0], [0, 0, -2]]

        # Act
        _, result_x, result_y = find_best_move_target(board)

        # Assert
        expected_x = 2
        expected_y = 1
        self.assertTrue(expected_x == result_x)
        self.assertTrue(expected_y == result_y)


if __name__ == "__main__":
    unittest.main()
