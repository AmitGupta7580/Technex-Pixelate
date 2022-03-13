from pickle import FALSE, TRUE
import gym
import time
import pixelate_arena
import pybullet as p
import pybullet_data
import cv2
import os
import math

from Perception import Perception
from Controller import Controller, Direction

if __name__ == "__main__":
    parent_path = os.path.dirname(os.getcwd())
    os.chdir(parent_path)
    env = gym.make("pixelate_arena-v0")
    perception = Perception(env)
    controller = Controller(env, perception)
    time.sleep(0.5)

    # mission
    qualifier_path = [2, 1, 2, 3, 2, 4, 4, 5, 5, 1, 0, 1, 0, 0, 1, 1, 1, 2]
    finals_path = [3, 4, 3, 2, 1, 2, 3, 4, 4, 5, 5, 4, 1, 2, 2, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 5, 5, 5, 5, 5, 5, 4, 4, 3, 4, 4, 4, 5, 2, 3, 3, 2, 1, 0, 1, 2, 0, 5, 3, 4, 3, 3, 3, 2, 3, 1, 2, 1, 1, 1, 0, 1]

    # perception.get_location()
    for i, path in enumerate(finals_path):
        controller.move_bot(path)
        if i == 22: # some number
            env.unlock_antidotes()
    
    # on inc 1st dis of far inc

    # anti-clockwise rotations
    # controller.set_heading(Direction.LEFT_BOTTOM, clockwise=False)
    # controller.set_heading(Direction.RIGHT_BOTTOM, clockwise=False)
    # controller.set_heading(Direction.RIGHT, clockwise=False)
    # controller.set_heading(Direction.RIGHT_TOP, clockwise=False)
    # controller.set_heading(Direction.LEFT_TOP, clockwise=False)
    # controller.set_heading(Direction.LEFT, clockwise=False)

    # clockwise-rotations
    # controller.set_heading(Direction.LEFT_TOP, clockwise=True)
    # controller.set_heading(Direction.RIGHT_TOP, clockwise=True)
    # controller.set_heading(Direction.RIGHT, clockwise=True)
    # controller.set_heading(Direction.RIGHT_BOTTOM, clockwise=True)
    # controller.set_heading(Direction.LEFT_BOTTOM, clockwise=True)
    # controller.set_heading(Direction.LEFT, clockwise=True)

    img = env.camera_feed()
    # cv2.imshow("img", img)
    cv2.imwrite("sample_arena_img.png",img)
    cv2.waitKey(0)