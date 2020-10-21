import pygame
import tkinter as tk
from tkinter import messagebox
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
        self.master = master
        self.heading = ('Courier', 28, 'bold')
        self.paragraph = ('Courier', 20)
        self.bg_primary = black
        self.bg_secondary = grey
        self.text_colour = white
        self.blue_button = blue
        self.red_button = red
        self.algorithms = ["DIJKSTRA", "BI-DIJKSTRA", "A-STAR"]
        self.set_up_tk()

    def set_up_tk(self):
        """
        Sets up the tkinter main window.
        """
        self.master.geometry('500x500')
        self.master.title("Path Finding Visualiser")

        bg_frame = tk.Frame(self.master, height=500,
                            width=500, bg=self.bg_primary)
        bg_frame.pack()

        bar_frame = tk.Frame(self.master, height=60,
                             width=500, bg=self.bg_secondary)
        bar_frame.place(relx=0.0, rely=0.0)
        bar_title = tk.Label(
            self.master, text='PATH FINDING', font=self.heading, bg=self.bg_secondary, fg=self.text_colour)
        bar_title.place(relx=0.23, rely=0.015)

        info = 'Choose an algorithm from the menu below, pick start and end points, add walls and bombs and see how path-finding works. Here, we can only move left, right, up or down!'
        info_message = tk.Message(self.master, text=info.upper(
        ), bg=self.bg_primary, fg=self.text_colour, highlightthickness=0, font=self.paragraph, width=480)
        info_message.place(relx=0.01, rely=0.12)

        algorithm_label = tk.Label(
            self.master, text='ALGORITHMS:', bg=self.bg_primary, fg=self.text_colour, font=self.paragraph)
        algorithm_label.place(relx=0.03, rely=0.63)

        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set('CHOOSE')
        algorithm_option = tk.OptionMenu(
            self.master, self.algorithm_var, *self.algorithms)
        algorithm_option.config(bg=self.bg_secondary)
        algorithm_option.config(fg=self.text_colour)
        algorithm_option.config(width=12)
        algorithm_option.config(activebackground=self.bg_secondary)
        algorithm_option.config(highlightthickness=0)
        algorithm_option.config(activeforeground=self.text_colour)
        algorithm_option.config(font=self.paragraph)
        algorithm_option.place(relx=0.5, rely=0.63)

        self.check_var = tk.IntVar()
        check_vis = tk.Checkbutton(self.master, text='VISUALISE SOLVING PROCESS',
                                   variable=self.check_var, onvalue=1, offvalue=0, font=self.paragraph,
                                   bg=self.bg_primary, fg=self.text_colour, selectcolor=self.bg_secondary,
                                   activebackground=self.bg_secondary, activeforeground=self.text_colour)
        check_vis.place(relx=0.03, rely=0.76)

        run_button = tk.Button(self.master, text='RUN', bg=self.blue_button, fg=self.text_colour,
                               font=self.paragraph, command=self.run_path_finding, width=13)
        run_button.place(relx=0.03, rely=0.86)

        quit_button = tk.Button(self.master, text='QUIT', bg=self.red_button, fg=self.text_colour,
                                font=self.paragraph, command=sys.exit, width=13)
        quit_button.place(relx=0.54, rely=0.86)

    def run_path_finding(self):
        """
        Fetch the algorithm choice and visualisation - create an obj of the Path Finding Vis.
        """
        alg, vis = self.algorithm_var.get(), self.check_var.get()
        if alg == 'CHOOSE':
            messagebox.showerror(
                "ERROR", "You have not picked an algorithm."
            )
            return
        choice = self.algorithms.index(alg)
        show_vis = False
        if vis == 1:
            show_vis = True
        self.master.destroy()
        obj = PathFindingVis(choice, show_vis)


class PathFindingVis:
    def __init__(self, choice, show_vis):
        """
        Initialises the pygame window and the algorithm based on the choice and calls upon 
        the function to get user input.
        """
        self.algorithms = ["DIJKSTRA", "BI-DIJKSTRA", "A-STAR"]
        self.alg_choice = choice
        self.show_vis = show_vis

        self.win_width = 620
        self.win_height = 645

        # start and end co-ordinates for the inner grid
        self.start_x = 40
        self.end_x = 580
        self.start_y = 60
        self.end_y = 600

        # size of each square and num squares
        self.size = 30
        self.n = 18

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
        self.clock = pygame.time.Clock()

        # data structures to use
        self.start_cell = ()
        self.end_cell = ()
        self.visited_cells = {}
        self.bomb_cells = {}
        self.wall_cells = {}
        self.user_choice = 0
        self.instructions = [
            'Choose a starting point and hit next!',
            'Choose an ending point and hit next!',
            'Click and drag cells to add walls!',
            'Add bombs to make cells twice as costly!'
        ]
        self.instruction_text = self.instructions[self.user_choice]

        # Misc pygame setup
        self.btn_size_x, self.btn_size_y = 70, 25
        self.skip_x, self.skip_y = self.start_x, self.end_y + 10
        self.next_x, self.next_y = self.end_x - self.btn_size_x, self.end_y + 10
        self.mouse_pressed = False
        self.shortest_path = []
        self.show_path = False
        self.button1_text = 'SKIP'
        self.button2_text = 'NEXT'

        self.load_images()
        self.load_font()

        # Initialise object of algorithm

        self.alg_obj = None

        # call user input
        self.get_user_input()

    def reset_ds(self):
        """
        Reset all the data structures used.
        """
        self.start_cell = ()
        self.end_cell = ()
        self.visited_cells = {}
        self.bomb_cells = {}
        self.wall_cells = {}
        self.user_choice = 0
        self.instruction_text = self.instructions[self.user_choice]

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
        self.stop_image = pygame.transform.scale(
            pygame.image.load(
                r'C:\Users\akush\Desktop\Programming\Projects\Path_Finding_Visualisation\images\stop.png'
            ),
            (self.size, self.size)
        )
        self.go_image = pygame.transform.scale(
            pygame.image.load(
                r'C:\Users\akush\Desktop\Programming\Projects\Path_Finding_Visualisation\images\go.png'
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
            r'C:\Users\akush\Desktop\Programming\Projects\Path_Finding_Visualisation\fonts\mono.ttf', 22)

    def draw_grid(self):
        """
        Displays the grid to the users, shows the start and end, the walls, the visited nodes etc.
        """
        self.screen.fill(self.primary_bg)

        # show instruction text on top
        text_to_show = self.text_font.render(
            self.instruction_text.upper(), True, self.text_colour)
        text_rec = text_to_show.get_rect(
            center=(self.win_width // 2, self.start_y // 2))
        self.screen.blit(text_to_show, text_rec)

        # draw grid
        pygame.draw.rect(self.screen, self.grid_colour, [
                         self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y])

        # draw path
        for cell in self.shortest_path:
            i, j = cell
            x, y = i * self.size + self.start_x, j * self.size + self.start_y
            pygame.draw.rect(self.screen, self.green_button,
                             [x, y, self.size, self.size])

        for i in range(self.n):
            for j in range(self.n):
                cell = (i, j)
                x, y = i * self.size + self.start_x, j * self.size + self.start_y
                if not self.show_path:
                    if self.visited_cells.get(cell, False):
                        pygame.draw.rect(self.screen, self.visited_colour, [
                            x, y, self.size, self.size])
                pygame.draw.rect(self.screen, self.primary_bg, [
                                 x, y, self.size, self.size], 1)
                if self.start_cell == cell:
                    self.screen.blit(self.go_image, (x, y))
                if self.end_cell == cell:
                    self.screen.blit(self.stop_image, (x, y))
                if self.wall_cells.get(cell, False):
                    self.screen.blit(self.wall_image, (x, y))
                if self.bomb_cells.get(cell, False):
                    self.screen.blit(self.bomb_image, (x, y))

        # skip and next buttons

        pygame.draw.rect(self.screen, self.red_button, [
                         self.skip_x, self.skip_y, self.btn_size_x, self.btn_size_y])
        skip_text = self.text_font.render(
            self.button1_text, True, self.text_colour)
        skip_rect = skip_text.get_rect(
            center=(
                self.skip_x + self.btn_size_x//2, self.skip_y+self.btn_size_y//2
            )
        )
        self.screen.blit(skip_text, skip_rect)

        algorithm_name = self.algorithms[self.alg_choice]
        alg_text = self.text_font.render(
            algorithm_name, True, self.text_colour)
        alg_rect = alg_text.get_rect(
            center=(
                self.win_width//2, self.end_y + (self.win_height-self.end_y)//2
            )
        )
        self.screen.blit(alg_text, alg_rect)

        pygame.draw.rect(self.screen, self.green_button, [
            self.next_x, self.next_y, self.btn_size_x, self.btn_size_y
        ])
        next_text = self.text_font.render(
            self.button2_text, True, self.text_colour)
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
            if not self.user_choice and not self.start_cell:
                self.instruction_text = 'You have not selected a start cell yet yet!'
                return
            if self.user_choice == 1 and not self.end_cell:
                self.instruction_text = 'You have not selected an end cell yet!'
                return
            self.user_choice += 1

        if self.user_choice <= 3:
            self.instruction_text = self.instructions[self.user_choice]

        if self.user_choice == 3:
            self.button2_text = 'RUN'

    def process_data(self):
        """
        Process the walls and bombs to create an adjacency list and weight list and create an obj of the algorithm.
        """
        adj_list = {}
        cost_list = {}
        for i in range(self.n):
            for j in range(self.n):
                cell = (i, j)
                if self.wall_cells.get(cell, False):
                    continue
                cost = 0 if not self.bomb_cells.get(cell, False) else 1
                adj_list[cell] = []
                cost_list[cell] = []
                # west
                if i - 1 >= 0 and not self.wall_cells.get((i - 1, j), False):
                    adj_list[cell].append((i - 1, j))
                    is_bomb = self.bomb_cells.get((i - 1, j), False)
                    connection_cost = 1 if not is_bomb else 2
                    cost_list[cell].append(connection_cost + cost)
                # east
                if i + 1 < self.n and not self.wall_cells.get((i + 1, j), False):
                    adj_list[cell].append((i + 1, j))
                    is_bomb = self.bomb_cells.get((i + 1, j), False)
                    connection_cost = 1 if not is_bomb else 2
                    cost_list[cell].append(connection_cost + cost)
                # north
                if j - 1 >= 0 and not self.wall_cells.get((i, j-1), False):
                    adj_list[cell].append((i, j-1))
                    is_bomb = self.bomb_cells.get((i, j-1), False)
                    connection_cost = 1 if not is_bomb else 2
                    cost_list[cell].append(connection_cost + cost)
                # south
                if j + 1 < self.n and not self.wall_cells.get((i, j+1), False):
                    adj_list[cell].append((i, j+1))
                    is_bomb = self.bomb_cells.get((i, j+1), False)
                    connection_cost = 1 if not is_bomb else 2
                    cost_list[cell].append(connection_cost + cost)
        return adj_list, cost_list

    def drive_solver(self):
        """
        Create an object and call upon the event loop with vis or not.
        """
        adj, cost = self.process_data()
        if self.alg_choice == 0:
            self.alg_obj = DijkstraAlgorithm(
                adj, cost, self.start_cell, self.end_cell)
        elif self.alg_choice == 1:
            self.alg_obj = BiDijkstraAlgorithm(
                adj, cost, self.start_cell, self.end_cell
            )
        else:
            self.alg_obj = AStarAlgorithm(
                adj, cost, self.start_cell, self.end_cell)
        if self.show_vis:
            self.solve_visualiser()
        else:
            self.solve()

    def tkinter_choose_alg(self):
        """
        Choose an algorithm from the list.
        """
        self.root = tk.Tk()
        self.root.geometry('450x300')
        main_frame = tk.Frame(self.root, bg=black, width=450, height=300)
        main_frame.pack()

        app_bar = tk.Frame(self.root, width=450, height=60, bg=grey)
        app_bar.place(relx=0, rely=0)

        heading = tk.Label(self.root, text='CHOOSE ALGORITHM',
                           font=('Courier', 22), bg=grey, fg=white)
        heading.place(relx=0.2, rely=0.04)

        alg_label = tk.Label(self.root, text="ALGORITHM:",
                             font=('Courier', 20), bg=black, fg=white)
        alg_label.place(relx=0.02, rely=0.3)
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set(self.algorithms[self.alg_choice])
        algorithm_option = tk.OptionMenu(
            self.root, self.algorithm_var, *self.algorithms)
        algorithm_option.config(bg=grey)
        algorithm_option.config(fg=white)
        algorithm_option.config(width=12)
        algorithm_option.config(activebackground=grey)
        algorithm_option.config(highlightthickness=0)
        algorithm_option.config(activeforeground=white)
        algorithm_option.config(font=("Courier", 20))
        algorithm_option.place(relx=0.44, rely=0.3)

        self.check_var = tk.IntVar()
        check_vis = tk.Checkbutton(self.root, text='VISUALISE SOLVING PROCESS',
                                   variable=self.check_var, onvalue=1, offvalue=0, font=('Courier', 20),
                                   bg=black, fg=white, selectcolor=grey,
                                   activebackground=grey, activeforeground=white)
        check_vis.place(relx=0.02, rely=0.55)

        submit_btn = tk.Button(self.root, text='SUBMIT', font=('Courier', 20),
                               width=12, fg=white, bg=blue, command=self.reset_or_retry)
        submit_btn.place(relx=0.3, rely=0.75)

        self.root.mainloop()

    def reset_or_retry(self):
        """
        Get the alg choice as well as choice to show visualisation and either reset or retry.
        """
        self.alg_choice = self.algorithms.index(self.algorithm_var.get())
        self.show_vis = True if self.check_var == 1 else False
        self.root.destroy()
        if self.reset:
            self.reset_ds()
            self.get_user_input()
        else:
            self.drive_solver()

    def solved_mouse_input(self, pos):
        """
        Handle user input once the algorithm finds the shortest path.
        """
        self.reset = None
        x_pos, y_pos = pos
        if self.skip_x <= x_pos <= self.skip_x + self.btn_size_x and self.skip_y <= y_pos <= self.skip_y + self.btn_size_y:
            # retry clicked
            self.reset = False
            self.tkinter_choose_alg()

        if self.next_x <= x_pos <= self.next_x + self.btn_size_x and self.next_y <= y_pos <= self.next_y + self.btn_size_y:
            # reset clicked
            self.reset = True
            self.tkinter_choose_alg()

    def solved_alg(self, found):
        """
        Once the algorithm has finished running, shows number of cells used, shortest 
        path etc. Handle for re-runs and quits etc.
        """
        if found:
            self.shortest_path = self.alg_obj.path
            self.instruction_text = 'The shortest path uses {} cells!'.format(
                len(self.shortest_path))
        else:
            self.instruction_text = 'Error: no path exists. Please try again.'
        self.button1_text = 'RERUN'
        self.button2_text = 'RESET'
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.solved_mouse_input(pos)
            self.draw_grid()
            pygame.display.update()
            self.clock.tick(30)

    def solve_visualiser(self):
        """
        Event loop to visualise the solving of the program.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            if not self.alg_obj.solver_vis():  # finished running
                self.show_path = True
                if self.alg_obj.found_path:
                    self.solved_alg(True)
                else:
                    self.solved_alg(False)
            if self.alg_choice != 1:
                self.visited_cells = self.alg_obj.proc
            else:  # bi_dijkstra
                self.visited_cells = {
                    **self.alg_obj.proc, **self.alg_obj.proc_r}
            self.draw_grid()
            pygame.display.update()
            self.clock.tick(30)

    def solve(self):
        """
        Solve without any visualiser, simply show shortest path when done.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            self.alg_obj.solver()
            if self.alg_obj.found_path:
                self.solved_alg(True)
            else:
                self.solved_alg(False)
            self.draw_grid()
            pygame.display.update()
            self.clock.tick(30)

    def get_user_input(self):
        """
        Gets the user input for the parameters like the start point, end point, walls etc
        """
        while self.user_choice <= 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pressed = True
                    pos = pygame.mouse.get_pos()
                    self.mouse_input(pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_pressed = False
                if event.type == pygame.MOUSEMOTION:
                    if self.mouse_pressed:
                        pos = pygame.mouse.get_pos()
                        self.mouse_input(pos)
            self.draw_grid()
            pygame.display.update()
            self.clock.tick(30)
        self.drive_solver()


if __name__ == '__main__':
    root = tk.Tk()
    obj = TkinterDriver(root)
    root.mainloop()
