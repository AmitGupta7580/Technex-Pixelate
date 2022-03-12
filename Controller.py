import os
import enum
import gym
import time
import cv2
import pixelate_arena
import pybullet as p
import pybullet_data

from Perception import Perception

class HeadDirection(enum.Enum):
    TOP = 0
    TOP_RIGHT = 1
    RIGHT_TOP = 2
    RIGHT = 3
    RIGHT_BOTTOM = 4
    BOTTOM_RIGHT = 5
    BOTTOM = 6
    BOTTOM_LEFT = 7
    LEFT_BOTTOM = 8
    LEFT = 9
    LEFT_TOP = 10
    TOP_LEFT = 11

class MotionDirection(enum.Enum):
    RIGHT_TOP = 0
    RIGHT = 1
    RIGHT_BOTTOM = 2
    LEFT_BOTTOM = 3
    LEFT = 4
    LEFT_TOP = 5

class Controller:

    def __init__(self, env = None, perception = None):
        '''
        Abstract Class for high level motion of husky robot
        '''
        self.env = env
        self.perception = perception
        self.head = HeadDirection.LEFT


    def set_velocity(self, velocities, duration):
        vlf, vrf, vlr, vrr = velocities
        start = time.time()
        while True:
            p.stepSimulation()
            self.env.move_husky(vlf, vrf, vlr, vrr)
            if time.time() - start >= duration:
                break
        p.stepSimulation()
        self.env.move_husky(0, 0, 0, 0)


    def move_bot(self, direction):
        '''
        Move Bot to next Cell according to direction
        '''
        if direction == MotionDirection.LEFT:
            self.set_heading(HeadDirection.LEFT)
        elif direction == MotionDirection.LEFT_TOP:
            self.set_heading(HeadDirection.TOP_LEFT)
        elif direction == MotionDirection.LEFT_BOTTOM:
            self.set_heading(HeadDirection.BOTTOM_LEFT)
        elif direction == MotionDirection.RIGHT:
            self.set_heading(HeadDirection.RIGHT)
        elif direction == MotionDirection.RIGHT_BOTTOM:
            self.set_heading(HeadDirection.BOTTOM_RIGHT)
        elif direction == MotionDirection.RIGHT_TOP:
            self.set_heading(HeadDirection.TOP_RIGHT)

        self.move_forward(4)


    def move_forward(self, cnt_cells):
        self.set_velocity((0.5, 0.5, 0.5, 0.5), 3.2*cnt_cells)


    def set_heading(self, heading):
        '''
        Change head of the bot
        '''
        angle = (heading.value - self.head.value + 12) % 12
        if (self.head.value - heading.value + 12) % 12 < angle:
            angle = -( (self.head.value - heading.value + 12) % 12 )
        
        if angle == 0:
            return

        controller.set_velocity((0.3, -0.1, 0.3, -0.1), 3.9)

        # rotate bot by 30*angle degree
        # vel = 0.5 # m/s
        # turn_duration = [0, 100, 1.48, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # for c in range(abs(angle)):
        #     self.set_velocity((0.001, -0.001, 0.001, -0.001), turn_duration[abs(angle)])

        self.head = heading
        

    def set_location(self, destination):
        '''
        Global Planner
        '''
        destination_row, destination_col = destination
        current_row, current_col = perception.get_location()
        paths = [MotionDirection.LEFT_TOP, MotionDirection.LEFT_TOP, MotionDirection.LEFT_TOP, MotionDirection.LEFT_TOP]
        # print(f"Destination Location : {destination}")
        # print(F"Current Location : ({current_row}, {current_col})")
        # self.set_heading(1)
        for path in paths:
            self.move_bot(path)
            break
        pass


    def set_to_origin(self):
        pass

if __name__ == "__main__":
    parent_path = os.path.dirname(os.getcwd())
    os.chdir(parent_path)
    env = gym.make("pixelate_arena-v0")
    perception = Perception(env)
    controller = Controller(env, perception)
    time.sleep(0.5)
    perception.scan_arena()
    controller.set_location((2, 6))
    img = env.camera_feed()
    cv2.imshow("img", img)
    cv2.imwrite("sample_arena_img.png",img)
    cv2.waitKey(0)