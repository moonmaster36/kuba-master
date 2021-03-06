import pygame
from player import Player
from board import Board


def get_p1_from_user():
    print("Enter information for Player 1")
    name = input("Name: ")
    marble_color = input("Marble Color: ")
    print()
    return Player(name, marble_color.upper())


def get_p2_from_user():
    print("Enter information for Player 2")
    name = input("Name: ")
    marble_color = input("Marble Color: ")
    print()
    return Player(name, marble_color.upper())


def calculate_direction(marble_coords, move_coords):
    row1 = marble_coords[0]
    col1 = marble_coords[1]
    row2 = move_coords[0]
    col2 = move_coords[1]
    out = None
    if row2 == row1 + 2 or row2 == row1 + 1:
        out = 'B'
    elif row2 == row1 - 2 or row2 == row1 - 1:
        out = 'F'
    elif col2 == col1 + 2 or col2 == col1 + 1:
        out = 'R'
    elif col2 == col1 - 2 or col2 == col1 - 1:
        out = 'L'
    return out


class Kuba:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, kuba_window):
        self.kuba_window = kuba_window
        self.board = Board(("p1", "W"), ("p2", "B"))
        self.selected_move_coords = None
        self.selected_marble_coords = None

    def get_board(self):
        return self.board

    def update_kuba_window(self):
        self.board.draw(self.kuba_window)
        pygame.display.update()

    def select(self, row, col, win):
        current_player = self.board.get_player(self.board.get_current_turn())
        marble = self.board.get_marble((row, col))
        if self.selected_marble_coords:
            self.selected_move_coords = (row, col)
            direction = calculate_direction(self.selected_marble_coords, self.selected_move_coords)

            successful_move = self.board.make_move(current_player.get_name(),
                                                   (self.selected_marble_coords[0], self.selected_marble_coords[1]),
                                                   direction)
            ko_rule_violated = self.board.get_ko_rule_violated()
            if not successful_move and ko_rule_violated:
                self.selected_marble_coords = None
                self.board.set_selected_marble_coords(None)
                self.selected_move_coords = None
                self.select(row, col, win)
                return True
            else:
                # Clear after successful move
                self.selected_marble_coords = None
                self.board.set_selected_marble_coords(None)
                self.selected_move_coords = None
                return False

        elif marble != " ":
            self.selected_marble_coords = (row, col)
            self.board.set_selected_marble_coords((row, col))
            return True
        else:
            self.selected_move_coords = None
            self.selected_marble_coords = None
            self.board.set_selected_marble_coords(None)
            return False

    def get_winner(self):
        return self.board.get_winner()
