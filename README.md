# Tetris

### About

This work aims to build a modern Tetris game that can interact with Reinforcement Learning agents. It can be also played by human and supports features such as **hard** **drop**, **hold** **queue** and **T-spin**.

### States

Two np array:
- main board: (10, 20)
- next queue: (5, 4, 4), 5 Tetromino

### Actions

Discrete, 8 actions:
- 0 : noop
- 1 : move left
- 2 : move right
- 3 : move down
- 4 : hard drop
- 5 : rotate counter-clockwise
- 6 : rotate clockwise
- 7 : hold/dequeue

### Install dependencies

    pip install -r requirements.txt

### Agent play with Gym RL environment

By default, horizon is set to 5000 steps for an episode.

    import tetris
    env = tetris.Tetris()
    (initial_board, initial_next_queue) = env.reset()
    (board, next_queue), score, done = env.step(env.action_space.sample())

### Agent play with GUI visualization

    import tetris
    gui = tetris.GameGUI(mode='agent')
    env = gui.get_env()
    gui.play()
    # this will implicitly reset env
    (initial_board, initial_next_queue) = gui.start_game()
    (board, next_queue), score, done = env.step(env.action_space.sample())

### GUI mode, human play

    python3 play.py

<p align="center">
  <img src="/imgs/gui.jpg" alt="GUI"/>
</p>
