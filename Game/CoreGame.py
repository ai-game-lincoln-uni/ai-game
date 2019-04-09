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
# import keras
import random
import NeuralNetwork as nn


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
turn = 0  # Variable to hold turn for UI
AI = False    # Variable for NN, set to 0 before loaded

# Text objects
large_text = pygame.font.Font('freesansbold.ttf', 115)
medium_text = pygame.font.Font('freesansbold.ttf', 50)
small_text = pygame.font.Font("freesansbold.ttf", 20)

def end_screen(player, turns):
    pygame.time.wait(100)
    main = True
    # Colour variables
    blue = (29, 92, 193)
    yellow = (255, 255, 0)
    dark_yellow = (210, 225, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    # Text surfaces for the title and button
    text_surface = medium_text.render("Player {} is the Winner in {} turns!".format(player, turns), True, black)
    text_surface1 = small_text.render("Return to main menu", True, black)

    # Make blue background
    screen.fill(blue)

    # Draws the title
    text_rect = text_surface.get_rect()
    text_rect.center = ((width/2),(height/2))
    screen.blit(text_surface, text_rect)

    # Loop to update end screen while in use
    while main:
        for event in pygame.event.get():
            if event.type != pygame.MOUSEMOTION:
                log.debug(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        # Variables to hold mouse interaction
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # If the button is under the cursor
        if 340+220 > mouse[0] > 340 and 550+50 > mouse[1] > 550:
            # Change button colour while it is under cursor
            pygame.draw.rect(screen, dark_yellow, (340,550,220,50))
            # Call the start of the game for replaying
            if click[0] == 1:
                start_game()
        else:
            # Draw the button as default
            pygame.draw.rect(screen, yellow, (340,550,220,50))

        # Draw the buttons text onto the button
        text_rect = text_surface1.get_rect()
        text_rect.center = ((340 + (220 / 2)), (550 + (50 / 2)))
        screen.blit(text_surface1, text_rect)

        # Update the end screen
        pygame.display.update()

def flattenAndExport(playfield):
    """
    Flattens the 2D array into a 1D array and exports this data to a text file
    :param playfield: The game's playfield
    :return:
    """

    global GatherMove
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


def exportPlay(column):
    """
    Converts play to an array and exports this data to a text file
    :param column: The players move
    :return:
    """


    global GatherMove
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
    """
    Flattens the playfield array
    :param playField: 2d array
    :return: 1d array
    """
    field_array = []

    for row in playField:
        for item in row:
                field_array.append(item)

    return field_array


def _get_AI_move(playField):
    """
    Gets the AIs next move
    :param playField:
    :return: int of move
    """

    global AI

    if not AI:
        log.error("No AI found")    # Ensures that an AI exists, does happen earlier as well, just making sure
        nn._construct("AI")
        nn._save_model("AI")
        log.info("AI constructed")
        AI = True

    field = _flatten_field(playField)
    print(np.array(field).shape)
    moves = nn._predict(field)    # Should return array eg: [0.1, 0.1, 0.3, 0.8, 0.4, 0.2, 0.1]

    best_move = np.argmax(moves)    # Returns location of highest val, only first occurrence

    while not _validate_move(playField, best_move):    # Ensures return value is valid
        moves[best_move] = 0.0
        if moves == np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
            for i in range(8):
                if _validate_move(playField, i):    # If AI fails, just uses next available slot
                    return i
            log.error("AI failed to return usable value")
            return False
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
    try:
        log.debug("P{}: Placing piece at [{}][{}]".format(player, row, col))
        playField[row][col] = player

        if GatherMove:    # Exports play if board exported
            exportPlay(col)
    except Exception as e:
        log.error("Failed to place piece: {}".format(e))
        return False


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
    return -1  # negative 1 = no space


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
    return False


def renderer(playField):
    """
    Inverts and prints out the play field

    :param playField: The play field
    :return: None
    """
    screen.fill((0, 0, 0))
    try:
        playField = np.flip(playField, 0)

        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                if not TestMode:
                    pygame.draw.rect(screen, (0, 89, 179), ((col*100), (row*100)+100, 100, 100))
                else:
                    pygame.draw.rect(screen, (210, 0, 252), ((col * 100), (row * 100) + 100, 100, 100))
        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                if playField[row][col] == 0:
                    pygame.draw.circle(screen, (0, 0, 0), ((col*100)+50, (row*100)+150), radius)
                if playField[row][col] == 1:
                    pygame.draw.circle(screen, (206, 22, 48), ((col*100)+50, (row*100)+150), radius)
                if playField[row][col] == 2:
                    pygame.draw.circle(screen, (255, 201, 23), ((col*100)+50, (row*100)+150), radius)
        playField = np.flip(playField, 0)

        ### User interface junk
        # Create all needed surfaces
        textSurfaces = {
            "title": small_text.render("Connect 4", True, (255, 255, 255)),
            "NullSpacer": small_text.render("Wooo im invisible", False, (0, 0, 0)),
            "turnNum": small_text.render("Turn: " + str(turn), True, (255, 255, 255)),
            "AIMode": small_text.render("AI: %s" % ("Active" if AIMode else "Disabled"), True, (255, 255, 255)),
            "TestMode": small_text.render("TestMode: %s" % ("Active" if TestMode else "Disabled"), True, (255, 255, 255)),
        }

        # starting positions
        posX = ROW_COUNT*100 + 200
        posY = 125
        # Iterate through all surfaces
        for key, value in textSurfaces.items():
            rect = textSurfaces[key].get_rect()
            rect.center = (posX, posY)
            posY += 25
            screen.blit(textSurfaces[key], rect)

        return True
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
        if AIMode and (turn % 2 == 0):
            return _get_AI_move(playField)
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
            while not _validate_move(playField, col):
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
    global AIMode
    global AI
    global turn

    log.info("Game Loop started")
    turn = 1
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
                                    end_screen(turn % 2 + 1, turn)
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
                    TestMode = not TestMode
                    renderer(playField)
                    pygame.display.flip()
                    log.debug("Test Mode set to {}".format(TestMode))
                if event.key == pygame.K_d:
                    DataGatherMode = not DataGatherMode
                    log.debug("Data Gather mode set to {}".format(DataGatherMode))
                if event.key == pygame.K_a:
                    AIMode = not AIMode
                    if AIMode and (not AI):
                        try:
                            # AI = keras.models.load_model('AI.model')    # If first time AI toggles, imports the NN
                            nn._construct("AI")
                            # nn._save_model("AI")
                            AI = True
                            log.info("Neural Network model loaded")
                        except:
                            log.error("Failed to load Neural Network model")
                            AIMode = False    # Ensures not trying to get info from absent AI
                    log.debug("AI mode set to {}".format(AIMode))

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
                        end_screen(turn % 2 + 1, turn)
                        pygame.time.wait(10)
                        
                        return
                    turn += 1
        unique, counts = np.unique(playField, return_counts=True)
        dictionary = dict(zip(unique, counts))
        try:
            if dictionary[0] == 0:
                return
        except KeyError:
            log.warning("Playfield full, restarting...")
            renderer(playField)
            pygame.display.update()
            return
        except ValueError:
            pass



def main_menu():
    """
    The main menu screen
    :return: None
    """
    # Escape condition if test mode is enabled
    if TestMode:
        return

    log.info("Loading main menu")
    main = True
    counter = 0
    difficulty = ["Easy", "Medium", "Hard"]
    # Variables to hold various colours
    blue = (29, 92, 193)
    white = (255, 255, 255)
    black = (0, 0, 0)
    yellow = (255, 255, 0)
    dark_yellow = (210, 225, 0)
    red = (255, 0, 0)
    dark_red = (210, 0, 0)
    # Renders text for each button
    text_surface = small_text.render(difficulty[counter], True, black)
    text_surface1 = large_text.render("Connect 4", True, black)
    text_surface2 = small_text.render("Play", True, black)
    text_surface3 = small_text.render("Quit", True, black)
    # Renders text for instructions
    Instructions1 = small_text.render("Instructions:", True, black)
    Instructions2 = small_text.render("Click to place a counter in the lowest available position in the column", True, black)
    Instructions3 = small_text.render("The next player will do the same", True, black)
    Instructions4 = small_text.render("To win get four counters of your colour in a diagonal or straight row of 4", True, black)
    
    screen.fill(blue)
    
    # Draws the main title
    text_rect = text_surface1.get_rect()
    text_rect.center = ((width/2),(height/4))
    screen.blit(text_surface1, text_rect)

    # Draws the instructions
    text_rect = Instructions1.get_rect()
    text_rect.center = ((width/2),(height/2 - 50))
    screen.blit(Instructions1, text_rect)
    text_rect = Instructions2.get_rect()
    text_rect.center = ((width/2),(height/2 - 25))
    screen.blit(Instructions2, text_rect)
    text_rect = Instructions3.get_rect()
    text_rect.center = ((width/2),(height/2))
    screen.blit(Instructions3, text_rect)
    text_rect = Instructions4.get_rect()
    text_rect.center = ((width/2),(height/2 + 25))
    screen.blit(Instructions4, text_rect)

    #Loop to update the main menu while it is in use
    while main:
        for event in pygame.event.get():
            if event.type != pygame.MOUSEMOTION:
                log.debug(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        # Variables to store mouse information
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # If statement to respond to users interaction with play button
        if 225+150 > mouse[0] > 225 and 550+50 > mouse[1] > 550:
            # Change button colour while it is under cursor
            pygame.draw.rect(screen, dark_yellow, (225,550,150,50))
            # End loop and take player to the game if they click play
            if click[0] == 1:
                screen.fill(black)
                main = False
        else:
            pygame.draw.rect(screen, yellow, (225,550,150,50))

        # If statement to respond to users interaction with quit button
        if 525+150 > mouse[0] > 525 and 550+50 > mouse[1] > 550:
            # Change button colour while it is under cursor
            pygame.draw.rect(screen, dark_red, (525,550,150,50))
            # Exit the game if the user presses quit
            if click[0] == 1:
                pygame.quit()
                quit()

        else:
            pygame.draw.rect(screen, red, (525,550,150,50))

        # If statement to respond to users interaction with difficulty button
        if 375+150 > mouse[0] > 375 and 450+50 > mouse[1] > 450:
            # Change button colour while it is under cursor
            pygame.draw.rect(screen, dark_yellow, (375,450,150,50))
            # Changes counter that corresponds with difficulty type if clicked
            if click[0] == 1:
                
                if counter == 2:
                    counter = 0
                else:
                    counter += 1
                # Renders text with new difficulty setting
                text_surface = small_text.render(difficulty[counter], True, black)
                pygame.time.wait(100)
        else:
            pygame.draw.rect(screen, yellow, (375,450,150,50))

        # Draws difficulty text onto button
        text_rect = text_surface.get_rect()
        text_rect.center = ((375 + (150 / 2)), (450 + (50 / 2)))
        screen.blit(text_surface, text_rect)

        # Draws play text onto button
        text_rect = text_surface2.get_rect()
        text_rect.center = ((225 + (150 / 2)), (550 + (50 / 2)))
        screen.blit(text_surface2, text_rect)

        # Draws quit text onto button
        text_rect = text_surface3.get_rect()
        text_rect.center = ((525 + (150 / 2)), (550 + (50 / 2)))
        screen.blit(text_surface3, text_rect)

        # Updates display
        pygame.display.update()

def start_game():
    """
    Initialises the game and begins the main loop

    :return: None
    """
    main_menu()
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
    while TestMode or DataGatherMode:
        start_game()

