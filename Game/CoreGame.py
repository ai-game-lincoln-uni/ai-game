"""
Name: CoreGame.py
Version: 0.01
Purpose: Basic Connect 4 game for AI group project
Author: Daniel Allen
Date: 07/02/19
"""
import numpy as np
import pprint
import contextlib
import math
with contextlib.redirect_stdout(None):
    import pygame
from logManager import log
import os
import keras
import random


ROW_COUNT = 6
COLUMN_COUNT = 7


AIMode = False
DataGatherMode = False
GatherMove = False
TestMode = False

log.debug("AI mode set to {}".format(AIMode))
log.debug("Data Gather mode set to {}".format(DataGatherMode))
log.debug("Test Mode set to {}".format(TestMode))
pygame.init()
width = (COLUMN_COUNT+2) * 100
height = (ROW_COUNT + 1) * 100
size = (width, height)
radius = int(100/2 - 5)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 AI Game")
logo_image = pygame.image.load("unnamed.png")
pygame.display.set_icon(logo_image)

if AIMode:
    AI = keras.models.load_model('AI.model')    #Loads the NN model as made and saved in basicNeuralNet.py


def flattenAndExport(playfield):
    """
    Flattens the 2D array into a 1D array and exports this data to a text file
    :param playfield: The game's playfield
    :return:
    """

    GatherMove = True    # The play made at this point to be recorded, for AI target data

    dataForExport = []  # Prepare a list for the data to be dumped into
    for row in playfield:
        for item in row:
            dataForExport.append(item)  # dump each item one by one into this new list

    # EXPORTING CODE #
    if not os.path.isdir("trainingData"):
        # Verify the desired folder exists, if not, create it
        log.debug("Training Data folder missing... creating")
        os.mkdir("trainingData")

    fileNum = 0
    try:
        while True:
            # this loop makes sure it wont overwrite an existing file, then writes
            filename = "trainingData/ExportedState{}.txt".format(fileNum)
            if os.path.isfile(filename):
                fileNum += 1
            else:
                f = open(filename, "w")
                f.write(str(dataForExport))
                f.close()
                log.info("Exported current state to {}".format(filename))
                return True
    except Exception as e:
        # Error handling ^-^
        log.error("Failed to export game state: {}".format(e))
        return False


def exportPlay(column):    #todo: Why this isn't being called?
    """
    Converts play to an array and exports this data to a text file
    :param column: The players move
    :return:
    """

    GatherMove = False    # Ensures that only plays after exported boards are recorded

    dataForExport = []  # Prepare a list for the data to be dumped into


    """
    #Intended AI output would be list of probabilities indicating best move
    #e.g: [0.1, 0.3, 0.5, 0.7, 0.5, 0.2, 0.1]
    #Would indicate best move to be 4th column
    """

    for i in range(0, 7):
        if column == i:
            dataForExport.append(1.0)    #For move at col 2 would result in [0,0,1,0,0,0,0]
        else:
            dataForExport.append(0.0)

    # EXPORTING CODE #
    if not os.path.isdir("trainingData"):
        # Verify the desired folder exists, if not, create it
        log.debug("Training Data folder missing... creating")
        os.mkdir("trainingData")


    fileNum = 0
    try:
        while True:
            # this loop makes sure it wont overwrite an existing file, then writes
            filename = "trainingData/ExportedMove{}.txt".format(fileNum)
            if os.path.isfile(filename):
                fileNum += 1
            else:
                f = open(filename, "w")
                f.write(str(dataForExport))
                f.close()
                log.info("Exported current state to {}".format(filename))
                return True
    except Exception as e:
        # Error handling ^-^
        log.error("Failed to export game state: {}".format(e))
        return False


def _flatten_field(playField):
    field_array = []

    for row in playField:
        for item in row:
                field_array.append(item)

    return field_array


def _get_AI_move(playField):

    field = _flatten_field(playField)
    moves = AI.predict(field)    #Should return array eg: [0.1, 0.1, 0.3, 0.8, 0.4, 0.2, 0.1]

    best_move = np.argmax(moves)    #Returns location of highest val, only first occurrence

    while not _validate_move(playField, best_move):
        moves[best_move] = 0.0
        best_move = np.argmax(moves)

    log.info("AI selected move at {}".format(best_move))
    return best_move


def _create_playField(x=6, y=7):
    """
    Creates a 2D matrix of zeros. Default size is 6X7

    :param x: int: X axis size
    :param y: int: Y axis Size
    :return: 2D int array
    """
    log.debug("Generating playfield with dimensions [{}][{}]".format(x, y))
    playField = np.zeros((x, y)) # uses numpy to create a 2d array of pure zeros (im being lazy)
    return playField


def _drop_piece(playField, row, col, player):
    """
    Places the piece onto the playField

    :param playField: The play field
    :param row: The target row
    :param col: The target column
    :param player: The player making the move
    :return: None
    """
    log.debug("P{}: Placing piece at [{}][{}]".format(player, row, col))
    playField[row][col] = player

    if DataGatherMode and GatherMove:
        exportPlay(col)


def _validate_move(playField, col):
    """
    Checks to make sure the move in question is possible

    :param playField: The play field
    :param col: The target column
    :return: bool representing if move possible
    """
    # A one liner that returns an equality boolean
    return playField[ROW_COUNT-1][col] == 0


def _get_next_open_row(playField, col):
    """
    Checks where the piece will land on this row

    :param playField: The play field
    :param col: The target column
    :return: int representing the row number
    """
    # Iterates through the rows finding the first row where there is no existing piece
    for i in range(ROW_COUNT):
        if playField[i][col] == 0:
            log.debug("Selected row {} for {}".format(i, col))
            return i
    return -1


def _winning_move(playField, player):
    """
    Checks if a player has won

    :param playField:
    :param player:
    :return:
    """
    # Check horizontal locations
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if (playField[row][col] == player and
                    playField[row][col+1] == player and
                    playField[row][col+2] == player and
                    playField[row][col+3] == player):
                return True
    # Check vertical locations
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if (playField[row][col] == player and
                    playField[row+1][col] == player and
                    playField[row+2][col] == player and
                    playField[row+3][col] == player):
                return True
    # check diagonal right slope
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if (playField[row][col] == player and
                    playField[row+1][col+1] == player and
                    playField[row+2][col+2] == player and
                    playField[row+3][col+3] == player):
                return True
    # check diagonal left slope
    for col in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if (playField[row][col] == player and
                    playField[row-1][col+1] == player and
                    playField[row-2][col+2] == player and
                    playField[row-3][col+3] == player):
                return True


def renderer(playField):
    """
    Inverts and prints out the play field

    :param playField: The play field
    :return: None
    """
    try:
        playField = np.flip(playField, 0)

        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                pygame.draw.rect(screen, (0, 89, 179), ((col*100), (row*100)+100, 100, 100))
        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                if playField[row][col] == 0:
                    pygame.draw.circle(screen, (0, 0, 0), ((col*100)+50, (row*100)+150), radius)
                if playField[row][col] == 1:
                    pygame.draw.circle(screen, (206, 22, 48), ((col*100)+50, (row*100)+150), radius)
                if playField[row][col] == 2:
                    pygame.draw.circle(screen, (255, 201, 23), ((col*100)+50, (row*100)+150), radius)
        playField = np.flip(playField, 0)
    except Exception as e:
        log.critical("Renderer failed with error {}".format(e))
        _quit(1)


def _quit(code=0):
    """Cleanly closes the game"""
    # In error codes, 0 = clean close, no errors
    # 1 = closed with errors, very bad
    if code == 1:
        log.critical("Game quiting with errors!")
    else:
        log.info("Game quiting...")
    pygame.display.quit()
    pygame.quit()
    exit(code)


def _input(playField, turn, pos):
    """
    Gets the player's move and validate it

    param playField: the play field
    :param turn: the current turn
    :return: the column the player chose
    """
    # If AI is enabled, this if statement will call ai to give a column number
    if TestMode:
        return random.randint(0, ROW_COUNT)
    if turn % 2 == 0 and AIMode:
        log.debug("Polling AI code for its move...")
        col = _get_AI_move(playField)
        """
        # todo: call some function that'll return a column number
        col = 0 # todo: remove this line
        return  # todo: remove this line and uncomment and edit the line below
        col = ["some function to get a value off the AI"]
        """

        ### SANITY CHECKS ###
        if col is None:
            log.critical("AI returned Null value")
            _quit(1)  # exit with an error condition
        try:
            int(col)
        except ValueError:
            log.critical("AI didnt return an int")
            _quit(1)  # exit with an error condition
        if col > COLUMN_COUNT-1:
            log.critical("AI returned an impossible position")
            _quit(1)  # exit with an error condition
        else:
            # value from the AI should be known good now, it can be used safely
            log.debug("AI is putting its piece on column {}".format(col))
            return col

    else:
        # if AIMode is not enabled, or its player 1, take input
        if turn%2 == 0 and DataGatherMode:
            col = random.sample([0, 1, 2, 3, 4, 5, 6], 1)
            while not _validate_move(playField, col):   # todo: <-- why not work?
                col = random.sample([0, 1, 2, 3, 4, 5, 6], 1)
            log.debug("Randomiser clicked at {}|{} = column: {}".format(pos[0], pos[1], col))
        else:
            posx = pos[0]
            col = int(math.floor(posx/100))
            if col > COLUMN_COUNT-1:
                return None
            log.debug("Player clicked at {}|{} = column: {}".format(pos[0], pos[1], col))
        return col


def _game_loop(playField):
    """
    The main game loop
    
    :param playField: the play field
    :return: 
    """
    global TestMode
    global DataGatherMode

    log.info("Game Loop started")
    turn = 0
    while True:
        # BIG SCARY EVENT LOOP!
        for event in pygame.event.get():  # poll pygame for events
            if event.type == pygame.QUIT:
                # Allow game to quit
                _quit()
            if not TestMode:
                if event.type == pygame.MOUSEMOTION:
                    # User moved the mouse, so move their piece after their cursor for  A E S T H E T I C S
                    pygame.draw.rect(screen, (0, 0, 0), (
                    0, 0, width, 100))  # hide the last frame of motion, turn this off for some really trippy stuff
                    posx = event.pos[0]  # get the location of the cursor
                    if posx < (COLUMN_COUNT * 100) - 25 and posx > 25:  # messy way of clamping the location above the game columns
                        if turn % 2 == 0:  # determine whos turn it is, and make the piece that colour
                            pygame.draw.circle(screen, (206, 22, 48), (posx, 50), int(radius))
                        else:
                            pygame.draw.circle(screen, (255, 201, 23), (posx, 50), int(radius))
                        pygame.display.update()  # refresh the screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # click = drop piece
                    col = _input(playField, turn, event.pos)  # determine what column the user clicked above
                    if col is not None:  # None = the user didnt click in a valid location, so we ignore it
                        row = _get_next_open_row(playField, col)  # determine what row we should place a piece
                        if row != -1:
                            _drop_piece(playField, row, col, turn % 2 + 1)  # drop said piece

                            if _winning_move(playField, turn % 2 + 1):  # check if a player has won
                                log.info("Win condition met for player {}".format(turn % 2 + 1))
                                renderer(playField)
                                print("Player {} is the Winner in {} turns!".format(turn % 2 + 1, turn))
                                if not TestMode:
                                    pygame.display.update()
                                    pygame.time.wait(2000)  # wait for a bit to allow the player to  B A S K  in their glory                       quit()
                                    return  # exit the game loop and quit
                                return
                        else:
                            log.info("Unable to place piece on column " + str(col))
                            turn -= 1
                        renderer(playField)
                        pygame.display.update()
                        turn += 1

            if event.type == pygame.KEYDOWN:
                # Bit of code for Mark, because he asked for the game to export its current state
                if event.key == pygame.K_F6 and turn%2==1:
                    # Check if the user pressed F6 then export
                    log.debug("Exporting current game state...")
                    flattenAndExport(playField)
                if event.key == pygame.K_t:
                    TestMode= not TestMode
                    log.debug("Test Mode set to {}".format(TestMode))
                if event.key == pygame.K_d:
                    DataGatherMode = not DataGatherMode
                    log.debug("Data Gather mode set to {}".format(DataGatherMode))

        if TestMode:
            col = _input(playField, turn, 1)
            if col is not None:  # None = the user didnt click in a valid location, so we ignore it
                row = _get_next_open_row(playField, col)  # determine what row we should place a piece
                if row != -1:
                    _drop_piece(playField, row, col, turn % 2 + 1)  # drop said piece
                    if _winning_move(playField, turn % 2 + 1):  # check if a player has won
                        log.info("Win condition met for player {}".format(turn % 2 + 1))
                        renderer(playField)
                        pygame.display.update()
                        print("Player {} is the Winner in {} turns!".format(turn % 2 + 1, turn))
                        pygame.time.wait(10)
                        return
                    turn += 1
        unique, counts = np.unique(playField, return_counts=True)
        dictionary = dict(zip(unique, counts))
        try:
            if  dictionary[0] == 0:
                return
        except KeyError:
            log.warning("Playfield full, restarting...")
            renderer(playField)
            pygame.display.update()
            return
        except ValueError:
            pass


def start_game():
    """
    Initialises the game and begins the main loop

    :return: None
    """
    log.info("Initialising game...")
    playField = _create_playField(ROW_COUNT, COLUMN_COUNT)  # Creates a playfield of size designated at the top of this file
    log.info("Rendering playfield...")
    if not TestMode:
        renderer(playField)  # Draw the User Interface
        pygame.display.update()  # Refresh the screen so drawing can be seen
    log.info("Ready!")
    _game_loop(playField)  # Start the game loop


if __name__ == "__main__":
    #  If the game is running itself (ie: someone didnt type ``import coreGame```), start the game
    start_game()
    while TestMode:
        start_game()
