import pygame
import tkinter as tk
import time
from colours import *
from dijkstra import *
from bi_dijkstra import *
from a_star import *
import sys


class TkinterDriver:
    def __init__(self, master):
        """
        Initialises the tkinter driver and gets user input from the user and calls upon the pygame window.
        """
        pass


class PathFindingVis:
    def __init__(self, choice, show_vis):
        """
        Initialises the pygame window and the algorithm based on the choice and calls upon 
        the function to get user input.
        """
        self.alg_choice = choice
        self.show_vis = show_vis

        self.win_width = 480
        self.win_height = 550

        # start and end co-ordinates for the inner grid
        self.start_x = 40
        self.end_x = 440
        self.start_y = 80
        self.end_y = 480

        # size of each square and num squares
        self.size = 20
        self.n = 20

        self.primary_bg = self.hex_to_colour(black)
        self.grid_colour = self.hex_to_colour(grey)
        self.visited_colour = self.hex_to_colour(blue_grey)
        self.text_colour = self.hex_to_colour(white)
        self.red_button = self.hex_to_colour(red)
        self.green_button = self.hex_to_colour(green)

        self.win_dimensions = self.win_width, self.win_height

        pygame.init()
        self.screen = pygame.display.set_mode(self.win_dimensions)
        pygame.display.set_caption("Path Finding")
        self.screen.fill(self.primary_bg)
        self.clock = pygame.time.Clock()

        # data structures to use
        self.start_cell = ()
        self.end_cell = ()
        self.visited_cells = {}
        self.bomb_cells = {}
        self.wall_cells = {}
        self.path_cells = {}
        self.user_choice = 0
        self.instructions = [
            'Choose a starting point and hit next!',
            'Choose an ending point and hit next!',
            'Click on a number of cells to create walls and hit next!',
            'Add bombs to make a cell more costly and hit run!'
        ]
        self.instruction_text = self.instructions[self.user_choice]

        # Misc pygame setup
        self.btn_size_x, self.btn_size_y = 60, 40
        self.skip_x, self.skip_y = self.start_x, self.end_y + 10
        self.next_x, self.next_y = self.end_x - self.btn_size_x, self.end_y + 10

        self.load_images()
        self.load_font()

        # Initialise object of algorithm

        self.alg_obj = None

        # call user input
        self.get_user_input()

    def hex_to_colour(self, hex):
        """
        Convert a hexadecimal colour into a tuple
        """
        red = int(hex[1:3], 16)
        blue = int(hex[3:5], 16)
        green = int(hex[5:7], 16)
        return (red, blue, green)

    def load_images(self):
        """
        Loads the images from the folders
        """
        self.bomb_image = pygame.transform.scale(
            pygame.image.load(
                r'C:\Users\akush\Desktop\Programming\Projects\Path_Finding_Visualisation\images\bomb.png'
            ),
            (self.size, self.size)
        )
        self.start_image = pygame.transform.scale(
            pygame.image.load(
                r'C:\Users\akush\Desktop\Programming\Projects\Path_Finding_Visualisation\images\start.png'
            ),
            (self.size, self.size)
        )
        self.finish_image = pygame.transform.scale(
            pygame.image.load(
                r'C:\Users\akush\Desktop\Programming\Projects\Path_Finding_Visualisation\images\finish.png'
            ),
            (self.size, self.size)
        )
        self.wall_image = pygame.transform.scale(
            pygame.image.load(
                r'C:\Users\akush\Desktop\Programming\Projects\Path_Finding_Visualisation\images\wall.png'
            ),
            (self.size, self.size)
        )

    def load_font(self):
        """
        Loads the font for the pygame display
        """
        self.text_font = pygame.font.Font(
            r'C:\Users\akush\Desktop\Programming\Projects\Path_Finding_Visualisation\fonts\mono.ttf', 18)

    def draw_grid(self, show_path):
        """
        Displays the grid to the users, shows the start and end, the walls, the visited nodes etc.
        """
        # show instruction text on top
        text_to_show = self.text_font.render(
            self.instruction_text.upper(), True, self.text_colour)
        text_rec = text_to_show.get_rect(
            center=(self.win_width // 2, self.start_y // 2))
        self.screen.blit(text_to_show, text_rec)

        # draw grid
        pygame.draw.rect(self.screen, self.grid_colour, [
                         self.start_x, self.start_y, self.end_x-self.start_x, self.end_y-self.start_y])
        for i in range(self.n):
            for j in range(self.n):
                cell = (i, j)
                x, y = i * self.size + self.start_x, j * self.size + self.start_y
                pygame.draw.rect(self.screen, self.primary_bg, [
                                 x, y, self.size, self.size], 1)
                if self.start_cell == cell:
                    self.screen.blit(self.start_image, (x, y))
                if self.end_cell == cell:
                    self.screen.blit(self.finish_image, (x, y))
                if self.wall_cells.get(cell, False):
                    self.screen.blit(self.wall_image, (x, y))
                if self.bomb_cells.get(cell, False):
                    self.screen.blit(self.bomb_image, (x, y))
                if not show_path:
                    if self.visited_cells.get(cell, False):
                        pygame.draw.rect(self.screen, self.visited_colour, [
                            x, y, self.size, self.size])
                else:
                    if self.path_cells.get(cell, False):
                        pygame.draw.rect(self.screen, self.green_button, [
                            x, y, self.size, self.size
                        ])

        # skip and next buttons

        pygame.draw.rect(self.screen, self.red_button, [
                         self.skip_x, self.skip_y, self.btn_size_x, self.btn_size_y])
        skip_text = self.text_font.render('SKIP', True, self.text_colour)
        skip_rect = skip_text.get_rect(
            center=(
                self.skip_x + self.btn_size_x//2, self.skip_y+self.btn_size_y//2
            )
        )
        self.screen.blit(skip_text, skip_rect)

        pygame.draw.rect(self.screen, self.green_button, [
            self.next_x, self.next_y, self.btn_size_x, self.btn_size_y
        ])
        n_t = 'NEXT'
        if self.user_choice == 3:
            n_t = 'RUN'
        next_text = self.text_font.render(n_t, True, self.text_colour)
        next_rect = next_text.get_rect(
            center=(
                self.next_x + self.btn_size_x//2, self.next_y + self.btn_size_y//2
            )
        )
        self.screen.blit(next_text, next_rect)

    def mouse_input(self, pos):
        """
        Get the mouse input, adjust the dictionaries
        """
        x_pos, y_pos = pos
        if self.start_x <= x_pos <= self.end_x and self.start_y <= y_pos <= self.end_y:
            # check which choice location
            x, y = (x_pos-self.start_x)//self.size, (y_pos -
                                                     self.start_y)//self.size
            if not self.user_choice:
                self.start_cell = (x, y)
            elif self.user_choice == 1:
                self.end_cell = (x, y)
            elif self.user_choice == 2:
                if (x, y) != self.start_cell and (x, y) != self.end_cell:
                    self.wall_cells[(x, y)] = True
            else:
                if (x, y) != self.start_cell and (x, y) != self.end_cell and not self.wall_cells.get((x, y), False):
                    self.bomb_cells[(x, y)] = True

        if self.skip_x <= x_pos <= self.skip_x + self.btn_size_x and self.skip_y <= y_pos <= self.skip_y + self.btn_size_y:
            # skip clicked
            if self.user_choice <= 1:
                self.instruction_text = 'Error: Cannot skip when choosing start or end!'
            else:
                self.user_choice += 1

        if self.next_x <= x_pos <= self.next_x + self.btn_size_x and self.next_y <= y_pos <= self.next_y + self.btn_size_y:
            # next clicked
            self.user_choice += 1
            self.instruction_text = self.instructions[self.user_choice]

    def process_data(self):
        """
        Process the walls and bombs to create an adjacency list and weight list and create an obj of the algorithm.
        """
        print(self.start_cell)
        print(self.end_cell)
        print(self.bomb_cells)
        print(self.wall_cells)
        sys.exit()

    def get_user_input(self):
        """
        Gets the user input for the parameters like the start point, end point, walls etc
        """
        while self.user_choice <= 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.mouse_input(pos)
            self.draw_grid(False)
            pygame.display.update()
            self.clock.tick(30)
        self.process_data()


if __name__ == '__main__':
    obj = PathFindingVis(0, True)
