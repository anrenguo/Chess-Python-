# Game module
# Contains all the game-related logic, including a main loop() function

# Imports
from sys import exit
from copy import copy
import pygame
import board as b
from constants import *

# Clock variable
clock = pygame.time.Clock()

# Font variables
big_font = pygame.font.SysFont('Comic Sans', 60)
medium_font = pygame.font.SysFont('Comic Sans', 50)
small_font = pygame.font.SysFont('Comic Sans', 25)

try:
    background_music = pygame.mixer.Sound(f'{SOUND_PATH}music.mp3') # Background music
    notify_sound = pygame.mixer.Sound(f'{SOUND_PATH}notify.mp3')    # For when a button is pressed
    move_sound = pygame.mixer.Sound(f'{SOUND_PATH}move.mp3')        # For when a move not resulting in a capture is made
    capture_sound = pygame.mixer.Sound(f'{SOUND_PATH}capture.mp3')  # For when a move resulting in a capture is made
    sounds = True   # To indicate that sounds are working
except pygame.error:
    sounds = False  # To indicate that sounds are not working

class Time:
    # Class that controls the game time
    def __init__(self, time):
        # Initialize white's and black's times depending on what argument was passed when initializing the class
        self.white = [time, True]   # The first value is the time, the second value states whether it is in normal or special time (True is normal)
        self.black = [time, True]   # Normal time: goes down normally. Special time: maximum value is 30 seconds, reverts back to 30 seconds after you make a move, if you run out of the 30 seconds you lose

    def update_time(self, player):
        # Updates time values
        if player == 'white':
            self.white[0] -= 1
        else:
            self.black[0] -= 1
        # If time has run out
        if self.white[0] < 0:
            if self.white[1]:   # If it is normal time, set the state to special time and the time back to 30
                self.white[1] = False
                self.white[0] = 30
            else:               # If it is special time, means someone lost
                return True
        if self.black[0] < 0:
            if self.black[1]:
                self.black[1] = False
                self.black[0] = 30
            else:
                return True

    def convert_time(self, seconds):
        # Converts a seconds input into a minutes and seconds input. Each return is two characters long
        minutes = seconds // 60
        seconds -= minutes * 60
        if minutes < 10:
            minutes = f'0{minutes}'
        if seconds < 10:
            seconds = f'0{seconds}'
        return str(minutes), str(seconds)


def get_promotion_choice(board, color):
    # Gets the promoting player's piece of choice to promote their pawn to
    box_width = 400
    box_height = 100
    start_x = DIMENSIONS[0] // 2 - box_width // 2
    start_y = DIMENSIONS[1] // 2 - box_height // 2
    pygame.draw.rect(b.window, MENU_COLOR, (start_x, start_y, box_width, box_height))
    pygame.draw.rect(b.window, BOX_COLOR, (start_x, start_y, box_width, box_height), 5)
    if color == 'white':
        options = (board.white_queen.image, board.white_rook.image, board.white_bishop.image, board.white_knight.image)
    else:
        options = (board.black_queen.image, board.black_rook.image, board.black_bishop.image, board.black_knight.image)
    # Draw the options onto the menu
    for i in range(4):
        b.window.blit(options[i], (start_x + i * 100 + 5, start_y + 5))
    pygame.display.flip()
    # While loop to wait for user to click a piece
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                if start_x <= mouse_position[0] < start_x + 100 and start_y <= mouse_position[1] <= start_y + 100:
                    return 'queen'
                elif start_x + 100 <= mouse_position[0] < start_x + 200 and start_y <= mouse_position[1] <= start_y + 100:
                    return 'rook'
                elif start_x + 200 <= mouse_position[0] < start_x + 300 and start_y <= mouse_position[1] <= start_y + 100:
                    return 'bishop'
                elif start_x + 300 <= mouse_position[0] <= start_x + 400 and start_y <= mouse_position[1] <= start_y + 100:
                    return 'knight'

def game_over(winner, victory_method):
    # Prints out a menu allowing the players to rematch or quit
    if winner == 'White':
        surface1 = big_font.render(f'{winner} won!', True, WHITE)
        surface2 = medium_font.render(f'By {victory_method}!', True, BLACK)
    elif winner == 'Black':
        surface1 = big_font.render(f'{winner} won!', True, BLACK)
        surface2 = medium_font.render(f'By {victory_method}!', True, WHITE)
    else:
        surface1 = big_font.render('Stalemate', True, CHARCOAL)
        surface2 = medium_font.render('Nobody won!', True, CHARCOAL)
    surface3 = small_font.render('Rematch', True, GHOST_WHITE)
    surface4 = small_font.render('Quit', True, GHOST_WHITE)
    pygame.draw.rect(b.window, MENU_COLOR, (DIMENSIONS[0] // 2 - 250, DIMENSIONS[1] // 2 - 200, 500, 360))
    pygame.draw.rect(b.window, BOX_COLOR, (DIMENSIONS[0] // 2 - 190, DIMENSIONS[1] // 2 + 60, 160, 60))
    pygame.draw.rect(b.window, BOX_COLOR, (DIMENSIONS[0] // 2 + 30, DIMENSIONS[1] // 2 + 60, 160, 60))
    if winner == 'White':
        b.window.blit(surface1, (DIMENSIONS[0] // 2 - 155, DIMENSIONS[1] // 2 - 150))
    elif winner == 'Black':
        b.window.blit(surface1, (DIMENSIONS[0] // 2 - 140, DIMENSIONS[1] // 2 - 150))
    else:
        b.window.blit(surface1, (DIMENSIONS[0] // 2 - 143, DIMENSIONS[1] // 2 - 150))
    if victory_method == 'checkmate':
        b.window.blit(surface2, (DIMENSIONS[0] // 2 - 166, DIMENSIONS[1] // 2 - 50))
    elif victory_method == 'timeout': 
        b.window.blit(surface2, (DIMENSIONS[0] // 2 - 133, DIMENSIONS[1] // 2 - 50))
    elif victory_method == 'resignation':
        b.window.blit(surface2, (DIMENSIONS[0] // 2 - 170, DIMENSIONS[1] // 2 - 50))
    else:
        b.window.blit(surface2, (DIMENSIONS[0] // 2 - 143, DIMENSIONS[1] // 2 - 50))
    b.window.blit(surface3, (DIMENSIONS[0] // 2 - 160, DIMENSIONS[1] // 2 + 72))
    b.window.blit(surface4, (DIMENSIONS[0] // 2 + 80, DIMENSIONS[1] // 2 + 72))
    pygame.display.flip()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                if DIMENSIONS[0] // 2 - 190 <= mouse_position[0] <= DIMENSIONS[0] // 2 - 30 and DIMENSIONS[1] // 2 + 60 <= mouse_position[1] <= DIMENSIONS[1] // 2 + 120:
                    # Rematch was chosen
                    if sounds:
                        notify_sound.play()
                    return False
                if DIMENSIONS[0] // 2 + 30 <= mouse_position[0] <= DIMENSIONS[0] // 2 + 190 and DIMENSIONS[1] // 2 + 60 <= mouse_position[1] <= DIMENSIONS[1] // 2 + 120:
                    # Quit was chosen
                    return True
    
def loop(time_choice):
    # Main game loop
    if sounds:
        # Start the background music
        background_music.play(-1)
        background_music.set_volume(0.1)
    def default_variables(time):
        # Define the default variable values
        return b.Board(), None, None, [], 'white', Time(time), 0
    board, available_moves, pawn_special, highlight_squares, turn, time, time_count = default_variables(time_choice)
    board.update_screen(time.convert_time(time.white[0]), time.convert_time(time.black[0]), highlight_squares, turn)
    def start():
        # Runs at the beginning and if the players choose to rematch
        surface = big_font.render('Start', True, WHITE)
        pygame.draw.rect(b.window, BOX_COLOR, (DIMENSIONS[0] // 2 - 150, DIMENSIONS[1] // 2 - 75, 300, 150))
        b.window.blit(surface, (DIMENSIONS[0] // 2 - 83, DIMENSIONS[1] // 2 - 42))
        while True:
            clock.tick(FPS)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_position = pygame.mouse.get_pos()
                    if DIMENSIONS[0] // 2 - 150 <= mouse_position[0] <= DIMENSIONS[0] // 2 + 150 and DIMENSIONS[1] // 2 - 75 <= mouse_position[1] <= DIMENSIONS[1] // 2 + 75:
                        if sounds:
                            notify_sound.play()
                        return
    start()
    while True:
        # Set the frame rate and update the screen
        clock.tick(FPS)
        board.update_screen(time.convert_time(time.white[0]), time.convert_time(time.black[0]), highlight_squares, turn)
        pygame.display.flip()
        time_count += 1
        if time_count == FPS:
            # If the increment has reached the FPS, means one second has passed
            time_count = 0
            if time.update_time(turn):
                # If someone lost due to timeout
                winner = 'Black' if turn == 'white' else 'White'    # The winner is whoever did not run out of time
                if game_over(winner, 'timeout'):
                    # Quit
                    pygame.quit()
                    return
                else:
                    # Rematch
                    board, available_moves, pawn_special, highlight_squares, turn, time, time_count = default_variables(time_choice)
                    board.update_screen(time.convert_time(time.white[0]), time.convert_time(time.black[0]), highlight_squares, turn)
                    start()
                    continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                if DIMENSIONS[0] + 25 <= mouse_position[0] <= DIMENSIONS[0] + 225 and DIMENSIONS[1] // 2 - 50 <= mouse_position[1] <= DIMENSIONS[1] // 2 + 50:
                    # If the resignation button was pressed
                    if sounds:
                        notify_sound.play()
                    winner = 'Black' if turn == 'white' else 'White'    # The winner is whoever did not press the resignation button
                    if game_over(winner, 'resignation'):
                        # Quit
                        pygame.quit()
                        return
                    else:
                        # Rematch
                        board, available_moves, pawn_special, highlight_squares, turn, time, time_count = default_variables(time_choice)
                        board.update_screen(time.convert_time(time.white[0]), time.convert_time(time.black[0]), highlight_squares, turn)
                        start()
                        continue
                chosen_item = board.locate_chosen_piece(mouse_position[0], mouse_position[1])   # Locate the specific row and column and piece that the user chose depending on where he/she clicked
                try:
                    # Try/except block was used to prevent TypeError
                    if (chosen_item[0], chosen_item[1]) in available_moves:
                        # If the chosen item is an available move
                        normal_update = True
                        if sounds:
                            if chosen_item[2] is None:
                                move_sound.play()
                            else:
                                if chosen_item[2] != 'special' and chosen_item[2].color == chosen_piece[2].color:
                                    move_sound.play()
                                else:
                                    capture_sound.play()
                        time_count = 0  # Reset time count
                        if turn == 'white':
                            if not time.white[1]:
                                # Reset time if special time
                                time.white[0] = 30
                        else:
                            if not time.black[1]:
                                time.black[0] = 30
                        highlight_squares = []  # Empty highlight_squares
                        if pawn_special is not None:
                            # If there is a special pawn square
                            if chosen_item[0] == pawn_special[0] and chosen_item[1] == pawn_special[1]:
                                # If the chosen square was the special square, then kill the pawn
                                if pawn_special[0] < 4:
                                    # Since it was a pawn's first move, the target pawn has to be on one horizontal half of the board. Therefore, this if/else statement checks the row of the move to determine where the target pawn is
                                    board.array[3][pawn_special[1]] = None
                                else:
                                    board.array[4][pawn_special[1]] = None
                            pawn_special = None # Remove the special pawn square
                        if chosen_piece[2].rook_castle:
                            # If the chosen piece had the rook_castle attribute, remove it
                            chosen_piece[2].rook_castle = False
                        if chosen_piece[2].pawn_first_move:
                            # If the chosen piece had the pawn_first_move attribute
                            chosen_piece[2].pawn_first_move = False # Remove it first
                            if abs(chosen_item[0] - chosen_piece[0]) == 2:
                                # If the displacement between the new y coordinate and the old y coordinate is two, means the pawn made the special move. Thus set pawn_special to the special square where the opposite side can go to take the pawn
                                pawn_special = ((chosen_item[0] + chosen_piece[0]) // 2, chosen_piece[1])
                        if chosen_piece[2].king_castle:
                            # If the chosen piece has the attribute king_castle
                            chosen_piece[2].king_castle = False # Remove it first
                            if chosen_item[1] in (0, 7):
                                # If the x coordinate is on the edges, the player chose a rook as the target
                                normal_update = False
                                if turn == 'white':
                                    # Castle depending on which square was chosen and reset the relevant variables
                                    if chosen_item[1] == 0:
                                        board.castle((7, 2), (7, 3), 'white')
                                    elif chosen_item[1] == 7:
                                        board.castle((7, 6), (7, 5), 'white')
                                else:
                                    if chosen_item[1] == 0:
                                        board.castle((0, 2), (0, 3), 'black')
                                    elif chosen_item[1] == 7:
                                        board.castle((0, 6), (0, 5), 'black')
                        if chosen_piece[2].type == 'pawn' and (chosen_item[0] == 0 or chosen_item[0] == 7):
                            # Pawn promotion trigger: chosen piece is a pawn and the target square is an edge tile
                            normal_update = False
                            # Temporarily update the screen
                            board.array[chosen_item[0]][chosen_item[1]] = chosen_piece[2]
                            board.array[chosen_piece[0]][chosen_piece[1]] = None
                            board.update_screen(time.convert_time(time.white[0]), time.convert_time(time.black[0]),
                                                highlight_squares, turn)
                            # Promote the pawn
                            board.promotion(turn, chosen_item[0], chosen_item[1], get_promotion_choice(board, turn))
                        # Update the board's values, reset the relevant variables and swap turns
                        if normal_update:
                            board.array[chosen_item[0]][chosen_item[1]] = chosen_piece[2]
                        board.array[chosen_piece[0]][chosen_piece[1]] = None
                        available_moves = None
                        chosen_piece = None
                        turn = 'black' if turn == 'white' else 'white'
                        if board.detect_moves(turn, pawn_special) == 'checkmate':
                            # If a checkmate was detected
                            # Update screen to show the move then go through the game over logic
                            board.update_screen(time.convert_time(time.white[0]), time.convert_time(time.black[0]), highlight_squares, turn)
                            winner = 'Black' if turn == 'white' else 'White'    # The winner is whoever did not run out of time
                            if game_over(winner, 'checkmate'):
                                # Quit
                                pygame.quit()
                                return
                            else:
                                # Rematch
                                board, available_moves, pawn_special, highlight_squares, turn, time, time_count = default_variables(time_choice)
                                board.update_screen(time.convert_time(time.white[0]), time.convert_time(time.black[0]), highlight_squares, turn)
                                start()
                                continue
                        elif board.detect_moves(turn, pawn_special) == 'stalemate':
                            # If a stalemate was detected
                            # Update the screen to show the move then go through the game over logic
                            board.update_screen(time.convert_time(time.white[0]), time.convert_time(time.black[0]), highlight_squares, turn)
                            if game_over(None, 'stalemate'):
                                # Quit
                                pygame.quit()
                                return
                            else:
                                # Rematch
                                board, available_moves, pawn_special, highlight_squares, turn, time, time_count = default_variables(time_choice)
                                board.update_screen(time.convert_time(time.white[0]), time.convert_time(time.black[0]), highlight_squares, turn)
                                start()
                                continue
                        continue
                except TypeError:
                    pass
                if chosen_item[2] not in (None, 'special') and chosen_item[2].color == turn:
                    # If the chosen item is not None or special, and the chosen item's color is the current player's color
                    highlight_squares = []  # Empty highlight_squares
                    # Find the available moves and set the chosen piece to the chosen item
                    available_moves = board.locate_available_moves(chosen_item[0], chosen_item[1], chosen_item[2], pawn_special)
                    chosen_piece = copy(chosen_item)
                    if available_moves != []:
                        # Filter out the moves, assuming there is at least one move
                        filtered = board.filter_available_moves(chosen_piece, available_moves)
                        available_moves = copy(filtered[0])
                        for move in available_moves:
                            # Do the relevant highlights
                            if board.array[move[0]][move[1]] == 'special':
                                highlight_squares.append((move[0], move[1], 1))
                            else:
                                highlight_squares.append((move[0], move[1], 0))
                        if filtered[1]:
                            # If there was detected a move that will result in check against the current player, then highlight the current player's king square in red
                            highlight_squares.append((board.find_king(turn)[0], board.find_king(turn)[1], 2))
