import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from gym import Env
import numpy as np
from tetromino import Piece


class Game(Env):
    """
    Tetris game environment that represents the core of tetris.
    Inputs:
        next_queue_size:   the length of next tertromino queue size
    Important Members:
        score:      score of current game
        piece:      current tetromino piece that player is controlling
        main_board: tetris game board (10x22), 2 rows are invisible to player
        next_queue: shapes that will be spawned in next steps
    """
    def __init__(self, next_queue_size=5):
        self.next_queue_size = next_queue_size
        self.init_game()

    def init_game(self):
        self.score = 0
        self.piece = None
        self.game_over = False
        # Initalize board
        self.main_board = np.zeros(shape=(10,22), dtype=int)
        # Initialize next queue
        self.next_queue = []
        for i in range(self.next_queue_size):
            self.next_queue.append(Piece(np.random.randint(7)))

    def next_queue_state(self):
        """
        returns shapes in ndarray of next queue.
        """
        nq = []
        for s in self.next_queue:
            s, _ = s.get()
            nq.append(s)
        return np.array(nq)

    def render(self, mode='human', close=False):
        if mode == 'gui':
            return self.look_board(), self.next_queue_state(), self.score

    def step(self, action):
        """
        Tetris game environment that represents the core of tetris.
        actions:
            0 : noop
            1 : move left
            2 : move right
            3 : move down
            4 : hard drop
            5 : rotate counter-clockwise
            6 : rotate clockwise
            7 : hold/dequeue
        return:
            state:      (main_board, next_queue)
            reward:     score
            done:       if game over
        """
        if self.game_over or self.piece is None:
            return (self.look_board(), self.next_queue_state()), self.score, self.game_over
        if action == 1:
            shape, pos, index = self.piece.try_move_left()
        elif action == 2:
            shape, pos, index = self.piece.try_move_right()
        elif action == 3:
            shape, pos, index = self.piece.try_move_down()
        elif action == 4:
            while True:
                shape, pos, index = self.piece.try_move_down()
                if self.check_piece(shape, pos):
                    self.piece.commit(pos, index)
                else:
                    break
        elif action == 5:
            shape, pos, index = self.piece.try_rotate_counter_clockwise()
        elif action == 6:
            shape, pos, index = self.piece.try_rotate_clockwise()
        # ignore other actions
        else:
            return (self.look_board(), self.next_queue_state()), self.score, self.game_over
        if self.check_piece(shape, pos):
            self.piece.commit(pos, index)
        else:
            # move down failed, piece landed
            if action == 3 or action == 4:
                s, p = self.piece.get()
                self.land_piece(s, p)
            # rotate failed, check spins
            elif action == 5 or action == 6:
                if self.check_piece(shape, (pos[0]+1, pos[1])):
                    self.piece.commit((pos[0]+1, pos[1]), index)
                elif self.check_piece(shape, (pos[0]-1, pos[1])):
                    self.piece.commit((pos[0]-1, pos[1]), index)
        return (self.look_board(), self.next_queue_state()), self.score, self.game_over

    def reset(self):
        self.init_game()
        self.spawn_piece()
        return (self.look_board(), self.next_queue_state())

    def get_score(self):
        return self.score

    def spawn_piece(self):
        if self.game_over:
            return
        assert self.piece == None, "double piece exisitence"
        self.piece = self.next_queue.pop()
        self.next_queue.insert(0, Piece(np.random.randint(7)))
        shape, pos = self.piece.get()
        if not self.check_piece(shape, pos):
            self.game_over = True

    def land_piece(self, shape, pos):
        """
        piece landed to board, this can happen when piece try to move down.
        save info to board and check clear lines.
        input:
            shape:  ndarray that represents the shape
            pos:    the top/left piece position on board
        """
        for i, line in enumerate(shape):
            for j, v in enumerate(line):
                if v > 0:
                    self.main_board[pos[0]+i, pos[1]+j] = v
        self.clear_lines(pos)
        self.piece = None
        self.spawn_piece()

    def clear_lines(self, pos):
        """
        check board to see if there are lines need to be cleared
        """
        top = pos[1]
        lines = []
        for j in range(top, min(top+4, 22)):
            for i in range(0, 10):
                if self.main_board[i, j] == 0:
                    break
                if i == 9 and self.main_board[i, j] > 0:
                    lines.append(j)
        clear_num = len(lines)
        if clear_num == 0:
            return
        for j in reversed(range(0, lines[-1]+1)):
            if j > clear_num-1:
                for i in range(0, 10):
                    self.main_board[i, j] = self.main_board[i, j-clear_num]
            else:
                for i in range(0, 10):
                    self.main_board[i, j] = 0
        self.scoring(clear_num)

    def scoring(self, num_lines, type='basic'):
        if type == 'basic':
            if num_lines == 1:
                self.score += 40
            elif num_lines == 2:
                self.score += 100
            elif num_lines == 3:
                self.score += 300
            elif num_lines == 4:
                self.score += 1200

    def look_board(self):
        """
        look at main board with current moving piece.
        only returns board that visible to player (10x20)
        """
        board = self.main_board.copy()
        if self.piece is not None and self.game_over is False:
            shape, pos = self.piece.get()
            for i, line in enumerate(shape):
                for j, v in enumerate(line):
                    if v > 0:
                        assert board[pos[0]+i, pos[1]+j] == 0, 'piece conflict on board'
                        board[pos[0]+i, pos[1]+j] = v
        return board[:,2:]

    def check_boundry(self, x, y):
        """
        Check if piece is outside of board boundary.
        """
        if x >= 0 and x <= 9 and y >= 0 and y <= 21:
            return True
        return False

    def check_piece(self, shape, pos):
        """
        Check if piece is valid on main board.
        input:
            shape:      np array that describes the tetromini piece
            pos:        [x, y] of the top-left block location
        return:
            True if valid False otherwise
        """
        checked_num = 0
        for i, line in enumerate(shape):
            for j, v in enumerate(line):
                if v > 0:
                    if not self.check_boundry(pos[0]+i, pos[1]+j):
                        return False
                    # Something already on board
                    if self.main_board[pos[0]+i, pos[1]+j] > 0:
                        return False
                    checked_num += 1
                    if checked_num == 4:
                        return True
