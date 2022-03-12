from pickle import FALSE, TRUE
import gym
import time
import pixelate_arena
import pybullet as p
import pybullet_data
import cv2
import os

from Perception import Perception
from Controller import Controller, MotionDirection

if __name__ == "__main__":
    parent_path = os.path.dirname(os.getcwd())
    os.chdir(parent_path)
    env = gym.make("pixelate_arena-v0")
    perception = Perception(env)
    controller = Controller(env, perception)
    time.sleep(0.5)

    # mission


    img = env.camera_feed()
    cv2.imshow("img", img)
    cv2.imwrite("sample_arena_img.png",img)
    cv2.waitKey(0)