# Tetris

### About

This work aims to build a modern Tetris game that can interact with Reinforcement Learning agents. It can be also played by human and supports features such as **hard** **drop**, **hold** **queue** and **T-spin**.

It is currently work in progress.

### Actions

    0 : noop
    1 : move left
    2 : move right
    3 : move down
    4 : hard drop
    5 : rotate counter-clockwise
    6 : rotate clockwise
    7 : hold/dequeue

### Import as Gym RL environment

    import tetris
    env = tetris.Game()
    env.reset()
    (board, next_queue), score, done = env.step(1)

### GUI mode, human playable

    python3 play.py

![gui](/imgs/gui.png "GUI")

### TODOs:

- implement hard drop
- implement hold and dequeue
- support boundary rotation
- support T-spin
