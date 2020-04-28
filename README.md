# Tetris

### About

This work aims to build a modern Tetris game that can interact with Reinforcement Learning agents. It can be also played by human and supports features such as **hard** **drop**, **hold** **queue** and **T-spin**.

### States

Depends on initial setting `flattened_observation`:
- **true**:  shape (280, ): contains all pixel states in 1-D array, useful for Linear (full-connected) models.
- **false**: shape (1, 10, 320): 2-D array (1 channel) concatenating main board and next queue for 5 tetromino, useful for Conv2D models.


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
    state = env.reset()
    state, reward, done = env.step(env.action_space.sample())

### Agent play with GUI visualization

    import tetris
    gui = tetris.GameGUI(mode='agent')
    env = gui.get_env()
    gui.play()
    # this will implicitly reset env
    state = gui.start_game()
    state, reward, done = env.step(env.action_space.sample())

### GUI mode, human play

    python3 play.py

<p align="center">
  <img src="/imgs/gui.jpg" alt="GUI"/>
</p>
