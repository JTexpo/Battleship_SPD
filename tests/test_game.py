import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest
from battleship_spd.game import BattleshipGame

class TestGame(unittest.TestCase):

    def test_fire_at_tile_hit(self):
        # Arrange
        game = BattleshipGame(3)
        player_id = 1
        ship_id = 1
        x_position = 1
        y_position = 1
        is_vertical = False
        _ = game._set_ship_location(player_id=player_id,ship_id=ship_id,x_position=x_position,y_position=y_position,is_vertical=is_vertical)

        # Act
        result = game.fire_at_tile(opponent_id=player_id,x_position=x_position,y_position=y_position)

        # Assert
        self.assertTrue(result)
    
    def test_fire_at_tile_miss(self):
        # Arrange
        game = BattleshipGame(3)
        player_id = 1
        ship_id = 1
        x_position = 1
        y_position = 1
        x_bad_position = 0
        y_bad_position = 0
        is_vertical = False
        _ = game._set_ship_location(player_id=player_id,ship_id=ship_id,x_position=x_position,y_position=y_position,is_vertical=is_vertical)

        # Act
        result = game.fire_at_tile(opponent_id=player_id,x_position=x_bad_position,y_position=y_bad_position)

        # Assert
        self.assertFalse(result)
    

if __name__ == '__main__':
    unittest.main()
