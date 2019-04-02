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

### Install dependencies

    pip install -r requirements.txt

### Import as Gym RL environment

    import tetris
    env = tetris.Game()
    env.reset()
    (board, next_queue), score, done = env.step(env.action_space.sample())

### GUI mode, human playable

    python3 play.py

<p align="center">
  <img src="/imgs/gui.jpg" alt="GUI"/>
</p>

### TODOs:

- agent play visualization
