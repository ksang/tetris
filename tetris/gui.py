import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

import tkinter as tk
from tkinter import Canvas, Label, Tk, Text, Menu
from game import Game
import numpy as np
import time


GUI_WIDTH = 800
GUI_HEIGHT = 800
# Frame per second
FPS=30
# auto drop interval in ms
DROP_INTERVAL = 1000

RED         = "#eb3323"
GREEN       = "#7ea956"
BLUE        = "#4d73bc"
LIGHTBLUE   = "#73fbfd"
YELLOW      = "#f5c142"
ORANGE      = "#e08244"
PURPLE      = "#693799"
BLACK       = "#000000"

class GameGUI(object):
    def __init__(self):
        # Init tetris game core
        self.tetris = Game(gui=True)
        self.game_started = False
        self.last_drop = 0
        self.next_queue_items = []
        self.shape_block_border = int(GUI_HEIGHT/400)
        self.shape_block_unit = int(GUI_HEIGHT/20)
        self.shape_block_size = int(GUI_HEIGHT/20) - 2*self.shape_block_border
        self.next_queue_offset = self.shape_block_unit*4+2*self.shape_block_border

    def init_gui(self):
        # Init windows and tetris board canvas
        self.window = Tk()
        self.window.title("Tetris")
        self.window.geometry('%dx%d' % (GUI_WIDTH, GUI_HEIGHT))
        self.main_board = Canvas(
                            self.window,
                            width=GUI_WIDTH/2,
                            height=GUI_HEIGHT)
        self.main_board.pack(side=tk.LEFT)
        self.main_board.config(bg='black')
        # Init menu
        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        tetrismenu = Menu(menubar)
        menubar.add_cascade(label = "Tetris", menu = tetrismenu)
        tetrismenu.add_command(label="Start", command=self.start_game)
        tetrismenu.add_command(label="Quit", command=self.window.quit)
        # Init side board
        self.side_board = Canvas(
                            self.window,
                            width=GUI_WIDTH/2,
                            height=GUI_HEIGHT)
        self.side_board.pack(side=tk.LEFT)
        self.side_board.config(bg='white')
        # help text
        help_text = """a : move left
d : move right
s : move down
w : hard drop
j : rotate counter-clockwise
k : rotate clockwise
l : hold"""
        self.side_board.create_text(int(GUI_HEIGHT*3/8), 80, text=help_text)
        # Display score
        self.score = self.side_board.create_text(50, GUI_HEIGHT-20,
                                        text="Score: 0",
                                        font="Arial 20 bold")

        # Next queue backgrounds
        self.side_board.create_rectangle(0,0,
                            self.shape_block_unit*4,
                            self.shape_block_unit*4,
                            outline=BLACK, fill=BLACK)
        self.side_board.create_rectangle(0,
                            self.next_queue_offset,
                            self.shape_block_unit*4,
                            self.shape_block_unit*4+self.next_queue_offset,
                            outline=BLACK, fill=BLACK)
        self.side_board.create_rectangle(0,
                            2*self.next_queue_offset,
                            self.shape_block_unit*4,
                            self.shape_block_unit*4+2*self.next_queue_offset,
                            outline=BLACK, fill=BLACK)
        # Bind events
        self.window.bind("<KeyPress>", self.gui_game_start)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        tetrismenu.bind("<Button-1>", self.stop_game)

    def on_closing(self):
        self.window.quit()

    def update_score(self):
        self.side_board.itemconfig(self.score, text="Score: " + str(self.tetris.get_score()))

    def gui_game_start(self, key):
        if key.char == 'a':
            #print("move left")
            self.tetris.step(1)
        elif key.char == 's':
            #print("move down")
            self.tetris.step(3)
        elif key.char == 'd':
            #print("move right")
            self.tetris.step(2)
        elif key.char == 'w':
            #print("hard drop")
            self.tetris.step(4)
        elif key.char == 'j':
            #print("rotate counter clock-wise")
            self.tetris.step(5)
        elif key.char == 'k':
            #print("rotate clock-wise")
            self.tetris.step(6)
        elif key.char == 'l':
            #print("hold")
            self.tetris.step(7)


    def draw_mainboard(self, main_board):
        # first delete all old items on main board
        self.main_board.delete(tk.ALL)
        # draw rectangles according to game state
        for i, v in enumerate(main_board):
            for j, c in enumerate(v):
                left = self.shape_block_unit*i+self.shape_block_border
                right = left+self.shape_block_size-self.shape_block_border
                top = self.shape_block_unit*j+self.shape_block_border
                bottom = top+self.shape_block_size-self.shape_block_border
                # Line of four
                if c == 1:
                    self.main_board.create_rectangle(left, top, right, bottom,
                        outline=BLUE, fill=BLUE)
                # S-shape (orientation 1)
                elif c == 2:
                    self.main_board.create_rectangle(left, top, right, bottom,
                        outline=RED, fill=RED)
                # S-shape (orientation 2)
                elif c == 3:
                    self.main_board.create_rectangle(left, top, right, bottom,
                        outline=LIGHTBLUE, fill=LIGHTBLUE)
                # T-shape
                elif c == 4:
                    self.main_board.create_rectangle(left, top, right, bottom,
                        outline=ORANGE, fill=ORANGE)
                # L-shape (orientation 1)
                elif c == 5:
                    self.main_board.create_rectangle(left, top, right, bottom,
                        outline=GREEN, fill=GREEN)
                # L-shape (orientation 2)
                elif c == 6:
                    self.main_board.create_rectangle(left, top, right, bottom,
                        outline=PURPLE, fill=PURPLE)
                # Cube
                elif c == 7:
                    self.main_board.create_rectangle(left, top, right, bottom,
                        outline=YELLOW, fill=YELLOW)
                else:
                    self.main_board.create_rectangle(left, top, right, bottom,
                        fill="black")

    def draw_nextqueue(self, next_queue):
        # first clear old items
        for i in self.next_queue_items:
            self.side_board.delete(i)
        self.next_queue_items.clear()
        # draw rectangles according to game state
        for queueid in range(1,4):
            shape = next_queue[-1*queueid]
            for i, line in enumerate(shape):
                for j, c in enumerate(line):
                    left = self.shape_block_unit*i+self.shape_block_border
                    right = left+self.shape_block_size-self.shape_block_border
                    top = self.shape_block_unit*j+self.shape_block_border+(queueid-1)*self.next_queue_offset
                    bottom = top+self.shape_block_size-self.shape_block_border
                    item = None
                    # Line of four
                    if c == 1:
                        item = self.side_board.create_rectangle(left, top, right, bottom,
                            outline=BLUE, fill=BLUE)
                    # S-shape (orientation 1)
                    elif c == 2:
                        item = self.side_board.create_rectangle(left, top, right, bottom,
                            outline=RED, fill=RED)
                    # S-shape (orientation 2)
                    elif c == 3:
                        item = self.side_board.create_rectangle(left, top, right, bottom,
                            outline=LIGHTBLUE, fill=LIGHTBLUE)
                    # T-shape
                    elif c == 4:
                        item = self.side_board.create_rectangle(left, top, right, bottom,
                            outline=ORANGE, fill=ORANGE)
                    # L-shape (orientation 1)
                    elif c == 5:
                        item = self.side_board.create_rectangle(left, top, right, bottom,
                            outline=GREEN, fill=GREEN)
                    # L-shape (orientation 2)
                    elif c == 6:
                        item = self.side_board.create_rectangle(left, top, right, bottom,
                            outline=PURPLE, fill=PURPLE)
                    # Cube
                    elif c == 7:
                        item = self.side_board.create_rectangle(left, top, right, bottom,
                            outline=YELLOW, fill=YELLOW)
                    if item is not None:
                        self.next_queue_items.append(item)
    def draw(self):
        last_run = time.time() * 1000
        if self.game_started:
            mb, nq, score = self.tetris.render(mode='gui')
            self.draw_mainboard(mb)
            self.draw_nextqueue(nq)
            self.update_score()
        draw_time = time.time() * 1000 - last_run
        next_run = max(int(1000/FPS-draw_time), 0)
        self.window.after(next_run, self.draw)

    def auto_drop(self):
        self.tetris.step(3)
        self.window.after(DROP_INTERVAL, self.auto_drop)

    def play(self):
        self.init_gui()
        self.draw()
        self.window.mainloop()

    def start_game(self):
        self.game_started = True
        self.tetris.reset()
        self.auto_drop()

    def stop_game(self):
        self.game_started = False