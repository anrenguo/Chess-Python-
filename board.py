# Board module
# Used by the game module, this module includes many useful functions interacting with the chess board

# Imports
from copy import copy
import pygame
from constants import *

# Initialize pygame, start the display, and set its caption
pygame.init()
window = pygame.display.set_mode((DIMENSIONS[0] + 250, DIMENSIONS[1]))
pygame.display.set_caption('Chess - Anren Guo')

font = pygame.font.SysFont('Helvetica', 60)

class Board:
    # Class that controls the board
    class Piece:
        # Class that controls the piece and contains its characteristics
        def __init__(self, color, type, image, pawn_first_move = False, king_castle = False, rook_castle = False):
            self.color = color                      # Its color
            self.type = type                        # The type of piece
            self.image = image                      # The related image
            self.pawn_first_move = pawn_first_move  # Controls whether the pawn can make a double move
            self.king_castle = king_castle          # Controls whether the king can castle
            self.rook_castle = rook_castle          # Controls whether the rook can castle

    def __init__(self):
        # Initialize the variables
        def image(type):
            # Returns the image scaled to the piece dimensions
            return pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}{type}.png'), PIECE_DIMENSIONS)
        # All the piece variables
        self.white_pawn = self.Piece('white', 'pawn', image('white-pawn'), pawn_first_move = True)
        self.white_knight = self.Piece('white', 'knight', image('white-knight'))
        self.white_bishop = self.Piece('white', 'bishop', image('white-bishop'))
        self.white_rook = self.Piece('white', 'rook', image('white-rook'), rook_castle = True)
        self.white_queen = self.Piece('white', 'queen', image('white-queen'))
        self.white_king = self.Piece('white', 'king', image('white-king'), king_castle = True)
        self.black_pawn = self.Piece('black', 'pawn', image('black-pawn'), pawn_first_move = True)
        self.black_knight = self.Piece('black', 'knight', image('black-knight'))
        self.black_bishop = self.Piece('black', 'bishop', image('black-bishop'))
        self.black_rook = self.Piece('black', 'rook', image('black-rook'), rook_castle = True)
        self.black_queen = self.Piece('black', 'queen', image('black-queen'))
        self.black_king = self.Piece('black', 'king', image('black-king'), king_castle = True)
        # The board
        self.array = [
            [copy(self.black_rook), copy(self.black_knight), copy(self.black_bishop), copy(self.black_queen), copy(self.black_king), copy(self.black_bishop), copy(self.black_knight), copy(self.black_rook)],
            [copy(self.black_pawn) for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [copy(self.white_pawn) for _ in range(8)],
            [copy(self.white_rook), copy(self.white_knight), copy(self.white_bishop), copy(self.white_queen), copy(self.white_king), copy(self.white_bishop), copy(self.white_knight), copy(self.white_rook)]
        ]

    def update_screen(self, white_time, black_time, highlight_squares, color):
        # Updates the display
        window.fill(BACKGROUND)
        for row in range(len(self.array)):
            for column in range(len(self.array[row])):
                if (row % 2 == 0 and column % 2 == 0) or (row % 2 == 1 and column % 2 == 1):
                    pygame.draw.rect(window, LIGHT_BOARD, (column * (DIMENSIONS[0] // 8), row * (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8)))
                else:
                    pygame.draw.rect(window, DARK_BOARD, (column * (DIMENSIONS[0] // 8), row * (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8)))
                if self.array[row][column] not in (None, 'special'):
                    window.blit(self.array[row][column].image, (column * (DIMENSIONS[0] // 8) + 5, row * (DIMENSIONS[0] // 8) + 5))
        white_surfaces = font.render('White', True, WHITE), font.render(f'{white_time[0]}:{white_time[1]}', True, WHITE)
        black_surfaces = font.render('Black', True, BLACK), font.render(f'{black_time[0]}:{black_time[1]}', True, BLACK)
        if color == 'white':
            # Different coloring depending on the color to indicate who would be resigning if the button were to be pressed
            resignation_surface = font.render('Resign', True, BLACK)
            pygame.draw.rect(window, WHITE, (DIMENSIONS[0] + 25, DIMENSIONS[1] // 2 - 50, 200, 100))
        else:
            resignation_surface = font.render('Resign', True, WHITE)
            pygame.draw.rect(window, BLACK, (DIMENSIONS[0] + 25, DIMENSIONS[1] // 2 - 50, 200, 100))
        window.blit(resignation_surface, (DIMENSIONS[0] + 33, DIMENSIONS[1] // 2 - 25))
        window.blit(white_surfaces[0], (DIMENSIONS[0] + 50, DIMENSIONS[1] // 2 - 300))
        window.blit(white_surfaces[1], (DIMENSIONS[0] + 50, DIMENSIONS[1] // 2 - 200))
        window.blit(black_surfaces[0], (DIMENSIONS[0] + 50, DIMENSIONS[1] // 2 + 150))
        window.blit(black_surfaces[1], (DIMENSIONS[0] + 50, DIMENSIONS[1] // 2 + 250))
        if highlight_squares != []:
            def highlight_square(row, column, special = False, check = False):
                # Highlights the given square, along with extra arguments if needed
                if special:
                    pygame.draw.rect(window, SPECIAL_HIGHLIGHT, (column * (DIMENSIONS[0] // 8), row * (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8)))
                if check:
                    pygame.draw.rect(window, CHECK_HIGHLIGHT, (column * (DIMENSIONS[0] // 8), row * (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8)))
                if not special and not check:
                    if (row % 2 == 0 and column % 2 == 0) or (row % 2 == 1 and column % 2 == 1):
                        pygame.draw.rect(window, LIGHT_HIGHLIGHT, (column * (DIMENSIONS[0] // 8), row * (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8)))
                    else:
                        pygame.draw.rect(window, DARK_HIGHLIGHT, (column * (DIMENSIONS[0] // 8), row * (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8), (DIMENSIONS[0] // 8)))
                if self.array[row][column] not in (None, 'special'):
                    window.blit(self.array[row][column].image, (column * (DIMENSIONS[0] // 8) + 5, row * (DIMENSIONS[0] // 8) + 5))
            for square in highlight_squares:
                if square[2] == 0:
                    highlight_square(square[0], square[1])
                elif square[2] == 1:
                    highlight_square(square[0], square[1], special = True)
                elif square[2] == 2:
                    highlight_square(square[0], square[1], check = True)

    def on_board(self, row, column):
        # Finds whether the entered row and column is on the board
        if -1 < row < 8 and -1 < column < 8:
            return True # Returns True if on the board
        return False    # Returns False otherwise

    def locate_chosen_piece(self, x, y):
        # Locate which piece was chosen
        column = x // (DIMENSIONS[0] // 8)
        row = y // (DIMENSIONS[0] // 8)
        if self.on_board(row, column):
            return row, column, self.array[row][column]
        return None, None, None # Return an empty tuple if the chosen place is not on the board (to avoid errors when calling this function)

    def diagonal_moves(self, row, column, color):
        # Return all the possible diagonal moves
        diagonal_moves = []
        r = row + 1
        c = column + 1
        while self.on_board(r, c):
            if self.array[r][c] is not None:
                if self.array[r][c] == 'special':
                    diagonal_moves.append((r, c))
                    r += 1
                    c += 1
                    continue
                if self.array[r][c].color == color:
                    break
                if self.array[r][c].color != color:
                    diagonal_moves.append((r, c))
                    break
            diagonal_moves.append((r, c))
            r += 1
            c += 1
        r = row - 1
        c = column - 1
        while self.on_board(r, c):
            if self.array[r][c] is not None:
                if self.array[r][c] == 'special':
                    diagonal_moves.append((r, c))
                    r -= 1
                    c -= 1
                    continue
                if self.array[r][c].color == color:
                    break
                if self.array[r][c].color != color:
                    diagonal_moves.append((r, c))
                    break
            diagonal_moves.append((r, c))
            r -= 1
            c -= 1
        r = row + 1
        c = column - 1
        while self.on_board(r, c):
            if self.array[r][c] is not None:
                if self.array[r][c] == 'special':
                    diagonal_moves.append((r, c))
                    r += 1
                    c -= 1
                    continue
                if self.array[r][c].color == color:
                    break
                if self.array[r][c].color != color:
                    diagonal_moves.append((r, c))
                    break
            diagonal_moves.append((r, c))
            r += 1
            c -= 1
        r = row - 1
        c = column + 1
        while self.on_board(r, c):
            if self.array[r][c] is not None:
                if self.array[r][c] == 'special':
                    diagonal_moves.append((r, c))
                    r -= 1
                    c += 1
                    continue
                if self.array[r][c].color == color:
                    break
                if self.array[r][c].color != color:
                    diagonal_moves.append((r, c))
                    break
            diagonal_moves.append((r, c))
            r -= 1
            c += 1
        return diagonal_moves
    
    def straight_moves(self, row, column, color):
        # Return all the possible straight moves
        straight_moves = []
        r = row + 1
        while self.on_board(r, column):
            if self.array[r][column] is not None:
                if self.array[r][column] == 'special':
                    straight_moves.append((r, column))
                    r += 1
                    continue
                if self.array[r][column].color == color:
                    break
                if self.array[r][column].color != color:
                    straight_moves.append((r, column))
                    break
            straight_moves.append((r, column))
            r += 1
        r = row - 1
        while self.on_board(r, column):
            if self.array[r][column] is not None:
                if self.array[r][column] == 'special':
                    straight_moves.append((r, column))
                    r -= 1
                    continue  
                if self.array[r][column].color == color:
                    break
                if self.array[r][column].color != color:
                    straight_moves.append((r, column))
                    break
            straight_moves.append((r, column))
            r -= 1
        c = column + 1
        while self.on_board(row, c):
            if self.array[row][c] is not None:  
                if self.array[row][c] == 'special':
                    straight_moves.append((row, c))
                    c += 1
                    continue
                if self.array[row][c].color == color:
                    break
                if self.array[row][c].color != color:
                    straight_moves.append((row, c))
                    break
            straight_moves.append((row, c))
            c += 1
        c = column - 1
        while self.on_board(row, c):
            if self.array[row][c] is not None: 
                if self.array[row][c] == 'special':
                    straight_moves.append((row, c))
                    c -= 1
                    continue 
                if self.array[row][c].color == color:
                    break
                if self.array[row][c].color != color:
                    straight_moves.append((row, c))
                    break
            straight_moves.append((row, c))
            c -= 1
        return straight_moves

    def locate_available_moves(self, row, column, piece, pawn_special):
        # Locate the available moves
        self.remove_specials()
        available_moves = []
        if pawn_special is not None:
            # Change the square to special if there is a pawn_special square
            self.array[pawn_special[0]][pawn_special[1]] = 'special'
        match piece.type:
            # Return the available moves depending on which piece was chosen
            case 'queen':
                return self.straight_moves(row, column, piece.color) + self.diagonal_moves(row, column, piece.color)
            case 'rook':
                return self.straight_moves(row, column, piece.color)
            case 'bishop':
                return self.diagonal_moves(row, column, piece.color)
            case 'knight':
                possible_moves = ((row + 2, column + 1),
                                (row + 2, column - 1),
                                (row - 2, column + 1),
                                (row - 2, column - 1),
                                (row + 1, column + 2),
                                (row + 1, column - 2),
                                (row - 1, column + 2),
                                (row - 1, column - 2))
                for move in possible_moves:
                    # For every possible move, check if it is on the board.
                    # If it is on the board, check if it is an enemy piece, empty, or special
                    # If it is any of these, add the move to available moves
                    # This logic is repeated several times for the other piece types below
                    if self.on_board(move[0], move[1]):
                        if self.array[move[0]][move[1]] not in (None, 'special'):
                            if self.array[move[0]][move[1]].color != piece.color:
                                available_moves.append(move)
                        else:
                            available_moves.append(move)
            case 'pawn':
                normal_moves = []   # The straight moves that do not kill
                if piece.color == 'white':
                    if self.on_board(row - 1, column):
                        if self.array[row - 1][column] is None:
                            normal_moves.append((row - 1, column))
                            if piece.pawn_first_move:
                                if self.array[row - 2][column] is None:
                                    # If it is the pawn's first move and the two squares in front of it are empty, append the 'jump' move to normal_moves
                                    normal_moves.append((row - 2, column))
                                else:
                                    # To ensure the length of normal_moves is greater than one
                                    normal_moves.append((-1, -1))
                            else:
                                normal_moves.append((-1, -1))
                    kill_moves = ((row - 1, column + 1), (row - 1, column - 1)) # The diagonal moves that kill
                    for move in normal_moves:
                        if self.on_board(move[0], move[1]):
                            if self.array[move[0]][move[1]] is None:
                                # If any of the normal_moves is an empty square, append it to available moves
                                available_moves.append(move)
                    for move in kill_moves:
                        if self.on_board(move[0], move[1]):
                            # If any of the kill_moves is an enemy piece or a special square, append it to available moves
                            if self.array[move[0]][move[1]] not in (None, 'special'):
                                if self.array[move[0]][move[1]].color != piece.color:
                                    available_moves.append(move)
                            else:
                                if self.array[move[0]][move[1]] == 'special':
                                    available_moves.append(move)
                else:
                    if self.on_board(row + 1, column):
                        if self.array[row + 1][column] is None:
                            normal_moves.append((row + 1, column))
                            if piece.pawn_first_move:
                                if self.array[row + 2][column] is None:
                                    normal_moves.append((row + 2, column))
                                else:
                                    normal_moves.append((-1, -1))
                            else:
                                normal_moves.append((-1, -1))
                    kill_moves = ((row + 1, column + 1), (row + 1, column - 1))
                    for move in normal_moves:
                        if self.on_board(move[0], move[1]):
                            if self.array[move[0]][move[1]] is None:
                                available_moves.append(move)
                    for move in kill_moves:
                        if self.on_board(move[0], move[1]):
                            if self.array[move[0]][move[1]] not in (None, 'special'):
                                if self.array[move[0]][move[1]].color != piece.color:
                                    available_moves.append(move)
                            else:
                                if self.array[move[0]][move[1]] == 'special':
                                    available_moves.append(move)
            case 'king':
                if piece.king_castle:
                    # See whether the castle move is available
                    if piece.color == 'white':
                        if self.array[7][0] is not None and self.array[7][0].rook_castle and self.array[7][1] is None and self.array[7][2] is None and self.array[7][3] is None:
                            # Check if the spaces between the rook and the king are empty
                            # Check if the piece is eligible for checking
                            # Check if the king's movement squares are safe (i.e. if the middle square between the king's current position and his new position is safe)
                            self.array[7][3] = copy(self.white_king)
                            self.array[7][4] = None
                            if not self.detect_king_vulnerability('white'):
                                available_moves.append((7, 0))
                            self.array[7][3] = None
                            self.array[7][4] = copy(self.white_king)
                        if self.array[7][7] is not None and self.array[7][7].rook_castle and self.array[7][5] is None and self.array[7][6] is None:
                            self.array[7][5] = copy(self.white_king)
                            self.array[7][4] = None
                            if not self.detect_king_vulnerability('white'):
                                available_moves.append((7, 7))
                            self.array[7][5] = None
                            self.array[7][4] = copy(self.white_king)
                    else:
                        if self.array[0][0] is not None and self.array[0][0].rook_castle and self.array[0][1] is None and self.array[0][2] is None and self.array[0][3] is None:
                            self.array[0][3] = copy(self.black_king)
                            self.array[0][4] = None
                            if not self.detect_king_vulnerability('black'):
                                available_moves.append((0, 0))
                            self.array[0][3] = None
                            self.array[0][4] = copy(self.black_king)
                        if self.array[0][7] is not None and self.array[0][7].rook_castle and self.array[0][5] is None and self.array[0][6] is None:
                            self.array[0][5] = copy(self.black_king)
                            self.array[0][4] = None
                            if not self.detect_king_vulnerability('black'):
                                available_moves.append((0, 7))
                            self.array[0][5] = None
                            self.array[0][4] = copy(self.black_king)
                possible_moves = ((row + 1, column),
                                  (row - 1, column),
                                  (row, column + 1),
                                  (row, column - 1),
                                  (row + 1, column + 1),
                                  (row + 1, column - 1),
                                  (row - 1, column + 1),
                                  (row - 1, column - 1))
                for move in possible_moves:
                    if self.on_board(move[0], move[1]):
                        if self.array[move[0]][move[1]] not in (None, 'special'):
                            if self.array[move[0]][move[1]].color != piece.color:
                                available_moves.append(move)
                        else:
                            available_moves.append(move)
        return available_moves
    
    def filter_available_moves(self, piece, moves):
        # Filters the moves by removing the moves that leads to the king becoming vulnerable
        flag = False    # Shows whether a move was removed. If no moves are removed, the function will return False
        for move in copy(moves):
            # For every move, it is made temporarily, checked for king vulnerability, then reverted
            temp = self.array[move[0]][move[1]]
            self.array[move[0]][move[1]] = piece[2]
            self.array[piece[0]][piece[1]] = None
            if self.detect_king_vulnerability(piece[2].color):
                # Remove the move if it results in the king becoming vulnerable and sets the flag to True, indicating that a move was removed
                flag = True
                moves.remove(move)
            self.array[move[0]][move[1]] = temp
            self.array[piece[0]][piece[1]] = piece[2]
        return moves, flag

    def remove_specials(self):
        # Removes any special square if there is one
        for row in range(len(self.array)):
            for column in range(len(self.array[row])):
                if self.array[row][column] == 'special':
                    self.array[row][column] = None
                    return  # As there is only a maximum of one special square at any time, the function can be exited if a special square was found and removed
    
    def promotion(self, color, row, column, piece_type):
        # Promotes a pawn to a queen, rook, bishop, or knight depending on piece_type
        match piece_type:
            case 'queen':
                self.array[row][column] = copy(self.white_queen) if color == 'white' else copy(self.black_queen)
            case 'rook':
                self.array[row][column] = copy(self.white_rook) if color == 'white' else copy(self.black_rook)
            case 'bishop':
                self.array[row][column] = copy(self.white_bishop) if color == 'white' else copy(self.black_bishop)
            case 'knight':
                self.array[row][column] = copy(self.white_knight) if color == 'white' else copy(self.black_knight)

    def castle(self, new_king, new_rook, color):
        # Move the king and the rook to their new positions, and empty their old positions
        if color == 'white':
            if new_king[1] == 2:
                self.array[7][0] = None
            else:
                self.array[7][7] = None
        else:
            if new_king[1] == 2:
                self.array[0][0] = None
            else:
                self.array[0][7] = None
        self.array[new_king[0]][new_king[1]] = copy(self.white_king) if color == 'white' else copy(self.black_king)
        self.array[new_king[0]][new_king[1]].king_castle = False
        self.array[new_rook[0]][new_rook[1]] = copy(self.white_rook) if color == 'white' else copy(self.black_rook)
        self.array[new_rook[0]][new_rook[1]].rook_castle = False
    
    def find_king(self, color):
        # Finds where the king is
        for row in range(len(self.array)):
            for column in range(len(self.array[row])):
                if self.array[row][column] not in (None, 'special'):
                    if self.array[row][column].type == 'king' and self.array[row][column].color == color:
                        return row, column

    def detect_king_vulnerability(self, color):
        # Detects if the king is vulnerable
        def is_vulnerable(position, color, danger):
            # Define a nested function that can check whether the king is vulnerable
            # Danger - which type(s) of pieces can kill the king if it is on the position square
            return self.on_board(position[0], position[1]) and self.array[position[0]][position[1]] not in (None, 'special') and self.array[position[0]][position[1]].color != color and self.array[position[0]][position[1]].type in danger
        king_position = self.find_king(color)
        if color == 'white':
            black_king_possibilities = ((king_position[0] + 1, king_position[1]),
                                        (king_position[0] - 1, king_position[1]),
                                        (king_position[0], king_position[1] + 1),
                                        (king_position[0], king_position[1] - 1),
                                        (king_position[0] + 1, king_position[1] + 1),
                                        (king_position[0] + 1, king_position[1] - 1),
                                        (king_position[0] - 1, king_position[1] + 1),
                                        (king_position[0] - 1, king_position[1] - 1))
            for possibilities in black_king_possibilities:
                if is_vulnerable(possibilities, color, 'king'):
                    # If there is a king in any of the possibilities that is not the current player's color, return True indicating that the current player's king is vulnerable
                    return True
            black_pawn_possibilities = ((king_position[0] - 1, king_position[1] + 1),
                                        (king_position[0] - 1, king_position[1] - 1))
            for possibilities in black_pawn_possibilities:
                if is_vulnerable(possibilities, color, 'pawn'):
                    return True
            black_knight_possibilities = ((king_position[0] + 2, king_position[1] + 1),
                                          (king_position[0] + 2, king_position[1] - 1),
                                          (king_position[0] - 2, king_position[1] + 1),
                                          (king_position[0] - 2, king_position[1] - 1),
                                          (king_position[0] + 1, king_position[1] + 2),
                                          (king_position[0] + 1, king_position[1] - 2),
                                          (king_position[0] - 1, king_position[1] + 2),
                                          (king_position[0] - 1, king_position[1] - 2))
            for possibilities in black_knight_possibilities:
                if is_vulnerable(possibilities, color, 'knight'):
                    return True
            black_diagonal_possibilities = self.diagonal_moves(king_position[0], king_position[1], color)
            for possibilities in black_diagonal_possibilities:
                if is_vulnerable(possibilities, color, ('bishop', 'queen')):
                    return True
            black_straight_possibilities = self.straight_moves(king_position[0], king_position[1], color)
            for possibilities in black_straight_possibilities:
                if is_vulnerable(possibilities, color, ('rook', 'queen')):
                    return True
        else:
            white_king_possibilities = ((king_position[0] + 1, king_position[1]),
                                        (king_position[0] - 1, king_position[1]),
                                        (king_position[0], king_position[1] + 1),
                                        (king_position[0], king_position[1] - 1),
                                        (king_position[0] + 1, king_position[1] + 1),
                                        (king_position[0] + 1, king_position[1] - 1),
                                        (king_position[0] - 1, king_position[1] + 1),
                                        (king_position[0] - 1, king_position[1] - 1))
            for possibilities in white_king_possibilities:
                if is_vulnerable(possibilities, color, 'king'):
                    return True
            white_pawn_possibilities = ((king_position[0] + 1, king_position[1] + 1),
                                        (king_position[0] + 1, king_position[1] - 1))
            for possibilities in white_pawn_possibilities:
                if is_vulnerable(possibilities, color, 'pawn'):
                    return True
            white_knight_possibilities = ((king_position[0] + 2, king_position[1] + 1),
                                          (king_position[0] + 2, king_position[1] - 1),
                                          (king_position[0] - 2, king_position[1] + 1),
                                          (king_position[0] - 2, king_position[1] - 1),
                                          (king_position[0] + 1, king_position[1] + 2),
                                          (king_position[0] + 1, king_position[1] - 2),
                                          (king_position[0] - 1, king_position[1] + 2),
                                          (king_position[0] - 1, king_position[1] - 2))
            for possibilities in white_knight_possibilities:
                if is_vulnerable(possibilities, color, 'knight'):
                    return True
            white_diagonal_possibilities = self.diagonal_moves(king_position[0], king_position[1], color)
            for possibilities in white_diagonal_possibilities:
                if is_vulnerable(possibilities, color, ('bishop', 'queen')):
                    return True
            white_straight_possibilities = self.straight_moves(king_position[0], king_position[1], color)
            for possibilities in white_straight_possibilities:
                if is_vulnerable(possibilities, color, ('rook', 'queen')):
                    return True

    def detect_moves(self, color, pawn_special):
        # Detects whether there is a checkmate or stalemate
        pieces = []
        if color == 'white':
            # Find all the pieces on color's side
            for row in range(len(self.array)):
                for column in range(len(self.array[row])):
                    if self.array[row][column] not in (None, 'special'):
                        if self.array[row][column].color == 'white':
                            pieces.append((row, column, copy(self.array[row][column])))
        else:
            for row in range(len(self.array)):
                for column in range(len(self.array[row])):
                    if self.array[row][column] not in (None, 'special'):
                        if self.array[row][column].color == 'black':
                            pieces.append((row, column, copy(self.array[row][column])))
        for piece in pieces:
            if self.filter_available_moves(piece, self.locate_available_moves(piece[0], piece[1], piece[2], pawn_special))[0] != []:
                # If there is a move for any piece then there is no checkmate or stalemate
                return
        # If there are no possible moves, then it means that it is either a checkmate or a stalemate
        if self.detect_king_vulnerability(color):
            # If the king is vulnerable, then it is checkmate
            return 'checkmate'
        # Otherwise, it is stalemate
        return 'stalemate'
