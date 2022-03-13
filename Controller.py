import os
import enum
import gym
import time
import cv2
import pixelate_arena
import pybullet as p
import pybullet_data

from Perception import Perception

class Direction(enum.Enum):
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
        self.head = Direction.LEFT.value


    def set_velocity(self, velocities, steps):
        vlf, vrf, vlr, vrr = velocities
        self.env.move_husky(vlf, vrf, vlr, vrr)
        for step in range(steps):
            p.stepSimulation()
        self.env.move_husky(0, 0, 0, 0)
        p.stepSimulation()


    def move_bot(self, direction):
        '''
        Move Bot to next Cell according to direction
        '''
        # set heading of robot accrding to motion
        clockwise, turns = True, ( direction - self.head + 6)%6
        if (self.head - direction + 6)%6 < ( direction - self.head + 6)%6:
            clockwise, turns = False, ( self.head - direction + 6)%6

        # clockwise, turns = False, ( self.head - direction + 6)%6
        sign = 1 if clockwise else -1
        for turn in range(1, turns+1):
            self.set_heading(Direction((self.head + sign*turn + 6) % 6), clockwise=clockwise)
        
        # img = self.env.camera_feed()
        # cv2.imshow("img", img)

        # destination_pixel = 

        self.move_forward(1)
        # img = self.env.camera_feed()
        # cv2.imshow("img", img)

        self.head = direction


    def move_forward(self, cnt_cells):
        self.set_velocity((0.5, 0.5, 0.5, 0.5), 4300 * cnt_cells)


    def set_heading(self, heading, clockwise = True):
        '''
        Change head of the bot
        '''
        if heading == Direction.LEFT and clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 500)
            self.set_velocity((0.3, -0.3, 0.3, -0.3), 3650)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 1780)
        elif heading == Direction.LEFT and not clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 520)
            self.set_velocity((-0.3, 0.3, -0.3, 0.3), 3650)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 1780)
        elif heading == Direction.LEFT_BOTTOM and clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 465)
            self.set_velocity((0.3, -0.3, 0.3, -0.3), 5000)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 350)
        elif heading == Direction.LEFT_BOTTOM and not clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 1850)
            self.set_velocity((-0.3, 0.3, -0.3, 0.3), 3650)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 490)
        elif heading == Direction.LEFT_TOP and clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 1850)
            self.set_velocity((0.3, -0.3, 0.3, -0.3), 3650)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 550)
        elif heading == Direction.LEFT_TOP and not clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 500)
            self.set_velocity((-0.3, 0.3, -0.3, 0.3), 5000)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 430)
        elif heading == Direction.RIGHT_BOTTOM and clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 1900)
            self.set_velocity((0.3, -0.3, 0.3, -0.3), 3650)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 550)
        elif heading == Direction.RIGHT_BOTTOM and not clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 300)
            self.set_velocity((-0.3, 0.3, -0.3, 0.3), 5000)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 420)
        elif heading == Direction.RIGHT_TOP and clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 370)
            self.set_velocity((0.3, -0.3, 0.3, -0.3), 5000)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 400)
        elif heading == Direction.RIGHT_TOP and not clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 1825)
            self.set_velocity((-0.3, 0.3, -0.3, 0.3), 3650)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 400)
        elif heading == Direction.RIGHT and clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 500)
            self.set_velocity((0.3, -0.3, 0.3, -0.3), 3650)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 1810)
        elif heading == Direction.RIGHT and not clockwise:
            self.set_velocity((0.3, 0.3, 0.3, 0.3), 600)
            self.set_velocity((-0.3, 0.3, -0.3, 0.3), 3650)
            self.set_velocity((-0.3, -0.3, -0.3, -0.3), 1800)
        

    def set_location(self, destination):
        '''
        Global Planner
        '''
        destination_row, destination_col = destination
        current_row, current_col = perception.get_location()
        print(f"Destination Location : {destination}")
        print(F"Current Location : ({current_row}, {current_col})")
        paths = [Direction.LEFT_TOP, Direction.LEFT_TOP, Direction.LEFT_TOP, Direction.LEFT_TOP]
        for path in paths:
            self.move_bot(path)
            break
        pass


    def set_to_origin(self):
        pass

if __name__ == "__main__":
    parent_path = os.path.dirname(os.getcwd())
    os.chdir(parent_path)
    # env = gym.make("pixelate_arena-v0")
    perception = Perception()
    controller = Controller(perception)
    # time.sleep(0.5)

    # img = env.camera_feed()
    # cv2.imshow("img", img)
    # cv2.imwrite("sample_arena_img.png",img)
    # cv2.waitKey(0)

    controller.move_bot(Direction.RIGHT_BOTTOM.value)
