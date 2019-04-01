import numpy as np


Shapes = {
    # Line of four
    0 : np.array([
        [
            [0,0,0,0],
            [1,1,1,1],
            [0,0,0,0],
            [0,0,0,0]
        ],
        [
            [0,1,0,0],
            [0,1,0,0],
            [0,1,0,0],
            [0,1,0,0]
        ]
    ]),
    # S-shape (orientation 1)
    1 : np.array([
        [
            [0,0,0,0],
            [2,2,0,0],
            [0,2,2,0],
            [0,0,0,0]
        ],
        [
            [0,0,2,0],
            [0,2,2,0],
            [0,2,0,0],
            [0,0,0,0]
        ]
    ]),
    # S-shape (orientation 2)
    2 : np.array([
        [
            [0,0,0,0],
            [0,3,3,0],
            [3,3,0,0],
            [0,0,0,0]
        ],
        [
            [0,3,0,0],
            [0,3,3,0],
            [0,0,3,0],
            [0,0,0,0]
        ]
    ]),
    # T-shape
    3 : np.array([
        [
            [0,0,0,0],
            [0,4,0,0],
            [4,4,4,0],
            [0,0,0,0]
        ],
        [
            [0,0,0,0],
            [0,4,0,0],
            [0,4,4,0],
            [0,4,0,0]
        ],
        [
            [0,0,0,0],
            [0,0,0,0],
            [4,4,4,0],
            [0,4,0,0]
        ],
        [
            [0,0,0,0],
            [0,4,0,0],
            [4,4,0,0],
            [0,4,0,0]
        ]
    ]),
    # L-shape (orientation 1)
    4 : np.array([
        [
            [0,0,0,0],
            [0,0,5,0],
            [5,5,5,0],
            [0,0,0,0]
        ],
        [
            [0,5,0,0],
            [0,5,0,0],
            [0,5,5,0],
            [0,0,0,0]
        ],
        [
            [0,0,0,0],
            [5,5,5,0],
            [5,0,0,0],
            [0,0,0,0]
        ],
        [
            [0,5,5,0],
            [0,0,5,0],
            [0,0,5,0],
            [0,0,0,0]
        ]
    ]),
    # L-shape (orientation 2)
    5 : np.array([
        [
            [0,0,0,0],
            [0,6,0,0],
            [0,6,6,6],
            [0,0,0,0]
        ],
        [
            [0,6,6,0],
            [0,6,0,0],
            [0,6,0,0],
            [0,0,0,0]
        ],
        [
            [0,0,0,0],
            [0,6,6,6],
            [0,0,0,6],
            [0,0,0,0]
        ],
        [
            [0,0,6,0],
            [0,0,6,0],
            [0,6,6,0],
            [0,0,0,0]
        ]
    ]),
    # Cube
    6 : np.array([
        [
            [0,0,0,0],
            [0,7,7,0],
            [0,7,7,0],
            [0,0,0,0]
        ]
    ])
}

class Piece(object):
    """
    Piece represents a tetromino, it contains all possible shapes of it.
    id:     which type of shape (0-6)
    pos:    positiion of this piece top-left block [x, y] (0 <= x <= 5, 0 <= y <= 15)
    """
    def __init__(self, id, pos=[3, 0]):
        self.shape = Shapes[id]
        self.index = 0
        self.pos = pos
        self.orientation_num = len(self.shape)


    def get(self):
        """
        Get shape and position from current piece
        return:
            np.array of current shape
            [x, y] of current position
        """
        return self.shape[self.index], self.pos

    def commit(self, pos, index):
        """
        Commit shape index and position to current piece
        Should be done after check boundries
        pos:    [x, y] of the new position
        index:  orientation index returned by move/rotate calls
        """
        self.pos = pos
        self.index = index

    def reset(self):
        self.index = 0
        self.pos = [3, 0]

    def try_move_down(self):
        """
        Try to move piece down one block
        return:
            np.array of next shape if moved down
            [x, y] next position if moved down
            next index if moved down
        """
        pos = [self.pos[0], self.pos[1]+1]
        return self.shape[self.index], pos, self.index

    def try_move_left(self):
        """
        Try to move piece left one block
        return:
            np.array of next shape if moved left
            [x, y] next position if moved left
            next index if moved left
        """
        pos = [self.pos[0]-1, self.pos[1]]
        return self.shape[self.index], pos, self.index

    def try_move_right(self):
        """
        Try to move piece right one block
        return:
            np.array of next shape if moved right
            [x, y] next position if moved right
            next index if moved right
        """
        pos = [self.pos[0]+1, self.pos[1]]

        return self.shape[self.index], pos, self.index

    def try_rotate_clockwise(self):
        """
        Try to rotate clockwise
        return:
            np.array of next shape if rotated
            [x, y] next position if rotated
            next index if rotated
        """
        index = (self.index+1) % self.orientation_num
        return self.shape[index], self.pos, index

    def try_rotate_counter_clockwise(self):
        """
        Try to rotate counter clockwise
        return:
            np.array of next shape if rotated
            [x, y] next position if rotated
            next index if rotated
        """
        index = (self.index-1) % self.orientation_num
        return self.shape[index], self.pos, index


# tests
if __name__ == '__main__':
    for i in range(10):
        si = np.random.randint(7)
        p = Piece(si)
        print("Shape " + str(si) + " initial state:")
        print(p.get())
        n_s, n_p, n_i = p.try_move_down()
        p.commit(n_p, n_i)
        print("moved down:")
        print(p.get())
        n_s, n_p, n_i = p.try_rotate_counter_clockwise()
        p.commit(n_p, n_i)
        print("rotate counter:")
        print(p.get())
        n_s, n_p, n_i = p.try_rotate_clockwise()
        p.commit(n_p, n_i)
        print("rotate:")
        print(p.get())
        n_s, n_p, n_i = p.try_rotate_clockwise()
        p.commit(n_p, n_i)
        print("rotate:")
        print(p.get())
        print("="*20)
