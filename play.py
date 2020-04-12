#!/usr/local/bin/python3
from tetris import GameGUI
import sys
import time
import argparse

cmd_parser = argparse.ArgumentParser(description=None)
cmd_parser.add_argument('-t', '--horizon', default=-1, type=int,
                        help='Max number of steps for an episode, -1 means infinity')
cmd_parser.add_argument('-a', '--agent', default=False, action='store_true',
                        help='Enable agent mode for GUI.')

if __name__ == '__main__':
    args = cmd_parser.parse_args()
    if args.agent:
        g = GameGUI(mode='agent', horizon=args.horizon)
        g.play()
        print("Input action (0-7) (q) to quit:")
        while True:
            c = sys.stdin.read(1)
            if c == 'q':
                break
            if c.isdigit():
                g.tetris.step(int(c))
                g.update_window()
        g.close()
    else:
        GameGUI(mode='human', horizon=args.horizon).play()
