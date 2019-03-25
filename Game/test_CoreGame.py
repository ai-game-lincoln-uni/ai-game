"""
Name: test_CoreGame.py
Purpose: Unit testing for AI group project
Author: Ally Garton
Date: 09/03/19
"""

# NOTE - all functions start by resetting the play field to its original empty 6x7
#      - this ensures any changes made by previous functions do not affect testing

import random
import numpy as np
import CoreGame

ROW_COUNT = 6
COLUMN_COUNT = 7

def test_flattenAndExport(): #DONE
    playField = CoreGame._create_playField(6, 7)
    
    # this function should always return true unless there is an error
    assert CoreGame.flattenAndExport(playField) == True


def test_exportplay(): #DONE
    playField = CoreGame._create_playField(6, 7)
    
    # this function should always return true for each column unless there is an error
    assert CoreGame.exportPlay(0) == True
    assert CoreGame.exportPlay(1) == True
    assert CoreGame.exportPlay(2) == True
    assert CoreGame.exportPlay(3) == True
    assert CoreGame.exportPlay(4) == True
    assert CoreGame.exportPlay(5) == True
    assert CoreGame.exportPlay(6) == True


def test__flatten_field(): #DONE
    playField = CoreGame._create_playField(6, 7)
    
    # flatten field should leave the field as a 1d array of 0s
    # this function confirms it is equal to an array of 42 0s (6x7)
    array = [0] * 42
    assert CoreGame._flatten_field(playField) == array


#def test__get_AI_move(): #?


def test__create_playField(): #DONE
    playField = CoreGame._create_playField(6, 7)

    # the assertion that the play field is a 2d array of 6x7 0s should return true
    # the actual _create_playField function is run and defined as a global variable
    np.testing.assert_equal(playField, np.zeros((6, 7)))


def test__drop_piece(): #DONE
    playField = CoreGame._create_playField(6, 7)

    # ensures that a random location at the start of the game will return false (no errors)
    # fills a column with pieces & ensures an error is thrown if more pieces are placed
    assert CoreGame._drop_piece(playField, 0, 3, 1) != False
    CoreGame._drop_piece(playField, 0, 2, 1)
    CoreGame._drop_piece(playField, 1, 2, 1)
    CoreGame._drop_piece(playField, 2, 2, 1)
    CoreGame._drop_piece(playField, 3, 2, 1)
    CoreGame._drop_piece(playField, 4, 2, 1)
    CoreGame._drop_piece(playField, 5, 2, 1)
    assert CoreGame._drop_piece(playField, 6, 2, 1) == False


def test__validate_move(): #DONE
    playField = CoreGame._create_playField(6, 7)

    # ensures the top row of the column (chosen ehre at random) is empty
    assert CoreGame._validate_move(playField, 3) == True

    # changes the top row of the column to a non-zero number (not empty)
    playField[ROW_COUNT - 1][3] = 1

    # confirms that the game returns False - the player cannot make that move
    assert CoreGame._validate_move(playField, 3) == False


def test__get_next_open_row(): #DONE
    playField = CoreGame._create_playField(6, 7)

    # initially finds a location on the field chosen at random
    # confirms it is set to 0
    assert CoreGame._get_next_open_row(playField, 3) == 0

    # changes first two locations in col 0 to non-zero numbers
    # confirms the game recognises this makes the next available row row 2
    playField[0][0] = 1
    playField[1][0] = 1
    assert CoreGame._get_next_open_row(playField, 0) == 2



def test__winning_move(): #DONE
    playField = CoreGame._create_playField(6, 7)

    # checks the default empty play field returns false
    assert CoreGame._winning_move(playField, 1) == False

    CoreGame._drop_piece(playField, 0, 0, 1)
    CoreGame._drop_piece(playField, 0, 1, 1)
    CoreGame._drop_piece(playField, 0, 2, 1)
    CoreGame._drop_piece(playField, 0, 3, 1)
    assert CoreGame._winning_move(playField, 1) == True

    playField = CoreGame._create_playField(6, 7)
    CoreGame._drop_piece(playField, 0, 0, 1)
    CoreGame._drop_piece(playField, 1, 0, 1)
    CoreGame._drop_piece(playField, 2, 0, 1)
    CoreGame._drop_piece(playField, 3, 0, 1)
    assert CoreGame._winning_move(playField, 1) == True

    playField = CoreGame._create_playField(6, 7)
    CoreGame._drop_piece(playField, 0, 0, 1)
    CoreGame._drop_piece(playField, 1, 1, 1)
    CoreGame._drop_piece(playField, 2, 2, 1)
    CoreGame._drop_piece(playField, 3, 3, 1)
    assert CoreGame._winning_move(playField, 1) == True

    playField = CoreGame._create_playField(6, 7)
    CoreGame._drop_piece(playField, 3, 3, 1)
    CoreGame._drop_piece(playField, 2, 2, 1)
    CoreGame._drop_piece(playField, 1, 1, 1)
    CoreGame._drop_piece(playField, 0, 0, 1)
    assert CoreGame._winning_move(playField, 1) == True



def test_renderer(): #DONE
    playField = CoreGame._create_playField(6, 7)

    # this function should always return true unless there is an error
    assert CoreGame.renderer(playField) == True


#def test__quit(): #?



#def test__input(): #?



#def test__game_loop(): #?



#def test_start_game(): #?


