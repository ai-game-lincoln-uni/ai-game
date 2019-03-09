import numpy as np
import CoreGame

ROW_COUNT = 6
COLUMN_COUNT = 7
playField = CoreGame._create_playField(6, 7)

def test__create_playField():
    np.testing.assert_equal(playField, np.zeros((6, 7)))

def test_flattenAndExport():
    assert CoreGame.flattenAndExport(playField) == True

#def test__drop_piece(CoreGame._create_playField(6, 7), 6, 7,

#def test__validate_move():
    #assert CoreGame._validate_move(playField, 3) == True
    #assert CoreGame._validate_move(playField, 5) == False

def test__get_next_open_row():
    assert CoreGame._get_next_open_row(playField, 3) == 0
    playField[0][0] = 1
    assert CoreGame._get_next_open_row(playField, 0) != 0

#def test__winning_move():
    #assert CoreGame._winning_move(playField, 1)
