import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from gym import Env
from gym.spaces import Discrete
from gym.spaces import Box
import numpy as np
from tetromino import Piece


class Tetris(Env):
    """
    Tetris game environment that represents the core of tetris.
    Inputs:
        horizon:                the max number of steps for an episode,
                                default = 5000, -1 means infinity
        next_queue_size:        the length of next tertromino queue size,
                                default=5
        flattened_observation:  if provide flattened observation as 1D array
                                rather than board and next queue, default=False
    Important Members:
        score:      score of current game
        piece:      current tetromino piece that player is controlling
        held_piece: piece that in the hold queue
        main_board: tetris game board (10x22), 2 rows are invisible to player
        next_queue: shapes that will be spawned in next steps
    """
    def __init__(self, horizon=5000, flattened_observation=False):
        self.horizon = horizon
        self.t = 0
        self.next_queue_size = 5
        self.flattened_observation = flattened_observation
        self.action_space = Discrete(8)
        if self.flattened_observation:
            # it is 10*20 because player only can see 10*20 board, top 2 lines are hidden
            self.observation_space = Box(0, 7, (10*20+4*4*self.next_queue_size,), np.int8)
        else:
            # it is 10*20 of main board, other 12 lines are next queue with padding
            self.observation_space = Box(0, 7, (10,20+4*3), np.int8)
        self.down_step_score = 1
        self.init_game()

    def init_game(self):
        self.score = 0
        self.t = 0
        self.piece = None
        self.held_piece = None
        # flag that indicates if current game is over
        self.game_over = False
        # flag that indicates if current piece is swapped of hold queue
        self.swapped = False
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
        print("Main board:")
        print(np.rot90(self.look_board(), 3))
        print("Next queue:")
        print(self.next_queue_state())
        print("Score:")
        print(self.score)

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
            reward:     score increased by this action
            done:       if game over
        """
        reward = 0
        if self.game_over or self.piece is None:
            return self.get_observation(), reward, self.game_over
        if action == 1:
            shape, pos, index = self.piece.try_move_left()
        elif action == 2:
            shape, pos, index = self.piece.try_move_right()
        elif action == 3:
            shape, pos, index = self.piece.try_move_down()
            proposed_score = self.down_step_score
        elif action == 4:
            while True:
                shape, pos, index = self.piece.try_move_down()
                if self.check_piece(shape, pos):
                    self.score += self.down_step_score
                    reward += self.down_step_score
                    self.piece.commit(pos, index)
                else:
                    break
        elif action == 5:
            shape, pos, index = self.piece.try_rotate_counter_clockwise()
        elif action == 6:
            shape, pos, index = self.piece.try_rotate_clockwise()
        # hold queue operations
        elif action == 7:
            # already swapped this turn, do nothing
            if self.swapped:
                pass
            # hold queue is empty
            elif self.held_piece is None:
                self.piece.reset()
                self.held_piece = self.piece
                self.piece = None
                self.spawn_piece()
            else:
                tmp = self.held_piece
                self.piece.reset()
                self.held_piece = self.piece
                self.piece = tmp
            shape, pos = self.piece.get()
            index = self.piece.index
            self.swapped = True
        # ignore other actions
        else:
            return self.get_observation(), reward, self.game_over
        if self.check_piece(shape, pos):
            self.score += reward
            self.piece.commit(pos, index)
        else:
            # move down failed, piece landed
            if action == 3 or action == 4:
                s, p = self.piece.get()
                reward += self.land_piece(s, p)
            # rotate failed, check spins
            elif action == 5 or action == 6:
                if self.check_piece(shape, (pos[0]+1, pos[1])):
                    self.piece.commit((pos[0]+1, pos[1]), index)
                elif self.check_piece(shape, (pos[0]-1, pos[1])):
                    self.piece.commit((pos[0]-1, pos[1]), index)
            # hold queue/dequeue failed, game over
            elif action == 7:
                self.game_over = True
        self.t += 1
        if self.horizon >= 0 and self.t >= self.horizon:
            self.game_over = True
        return self.get_observation(), reward, self.game_over

    def reset(self):
        self.init_game()
        self.spawn_piece()
        return self.get_observation()

    def get_score(self):
        return self.score

    def get_observation(self):
        """
        Convert observation to desired shape
        """
        if self.flattened_observation:
            return np.concatenate((self.look_board().reshape(-1,), self.next_queue_state().reshape(-1,)))
        nq = self.next_queue_state()
        nq_1 =  np.pad(np.concatenate((nq[0], nq[1]), axis=0), ((0,2),(0,0)),'constant')
        nq_2 =  np.pad(np.concatenate((nq[2], nq[3]), axis=0), ((0,2),(0,0)),'constant')
        nq_3 =  np.pad(nq[4], ((0,6),(0,0)),'constant')
        out = np.concatenate((self.look_board(), nq_1, nq_2, nq_3), axis=1)
        return out.reshape(1, out.shape[0], -1)

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
        return:
            bonus:  score increased by this land_piece action
        """
        for i, line in enumerate(shape):
            for j, v in enumerate(line):
                if v > 0:
                    self.main_board[pos[0]+i, pos[1]+j] = v
        bonus = self.clear_lines(pos)
        self.piece = None
        # reset hold queue flag
        self.swapped = False
        self.spawn_piece()
        return bonus

    def clear_lines(self, pos):
        """
        check board to see if there are lines need to be cleared
        return score increased by this land_piece action
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
            return 0
        for j in reversed(range(0, lines[-1]+1)):
            if j > clear_num-1:
                for i in range(0, 10):
                    self.main_board[i, j] = self.main_board[i, j-clear_num]
            else:
                for i in range(0, 10):
                    self.main_board[i, j] = 0
        return self.scoring(clear_num)

    def scoring(self, num_lines, type='basic'):
        bonus = 0
        if type == 'basic':
            if num_lines == 1:
                bonus = 40
            elif num_lines == 2:
                bonus = 100
            elif num_lines == 3:
                bonus = 300
            elif num_lines == 4:
                bonus = 1200
        self.score += bonus
        return bonus

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
