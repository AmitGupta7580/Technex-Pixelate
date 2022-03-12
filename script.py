import gym
import time
import pixelate_arena
import pybullet as p
import pybullet_data
import cv2
import os

from Perception import Perception
from Controller import Controller, HeadDirection

if __name__ == "__main__":
    parent_path = os.path.dirname(os.getcwd())
    os.chdir(parent_path)
    env = gym.make("pixelate_arena-v0")
    perception = Perception(env)
    controller = Controller(env, perception)
    time.sleep(0.5)
    perception.scan_arena()

    # Mission
    # Part-1 Go to Spiderman-2
    controller.set_velocity((0.3, -0.1, 0.3, -0.1), 3.9)
    time.sleep(0.2)
    # controller.set_heading(HeadDirection.TOP_LEFT)
    controller.move_forward(5)

    img = env.camera_feed()
    cv2.imshow("img", img)
    cv2.waitKey(0)