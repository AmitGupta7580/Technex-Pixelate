from turtle import position
import gym
import os
import time
import cv2
import enum
import numpy as np
import pixelate_arena

from helper import print_arena, filter

class Colors(enum.Enum):
    GREEN = ([27, 125, 33], [32, 130, 38])  # Goblin
    PURPLE = ([95, 10, 75], [100, 15, 80])  # Sandman
    YELLOW = ([0, 180, 225], [10, 185, 230])  # Electro
    PINK = ([160, 85, 225], [165, 90, 230])  # Antidodes
    WHITE = ([225, 225, 225], [230, 230, 230])  # Blocks
    RED = ([0, 15, 190], [5, 20, 195])  # Spiderman
    VILLAN = ([150, 60, 0], [155, 65, 5])  # Villans

class Perception:
    def __init__(self, env = None):
        '''
        Image Perception Class for Pixelate Arena
        '''
        self.env = env
        rows = 13
        cols = 25
        self.arena = [ [ 0 for j in range(cols) ] for i in range(rows) ]
        self.goblin = [(0, 0), (0, 0)]
        self.sandman = [(0, 0), (0, 0)]
        self.electro = [(0, 0), (0, 0)]
        self.antidodes = []
        self.spiderman = []

        # params
        self.y_pad = 44
        self.x_pad = 12
        self.hex_height = 39
        self.hex_width = 22.5

    def scan_arena(self):
        '''
        Decription of Arena:
        0 -> Empty Cell
        1 -> Whit Cell
        4 -> Goblin
        3 -> Sandman
        2 -> Electro
        5 -> Antidode
        6 -> Spiderman
        '''
        img = self.env.camera_feed()

        # Goblin
        out = filter(img, Colors.GREEN.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        positions = self.contours_to_location(contours)
        for position in positions:
            row, col = position
            self.arena[row][col] = 4

        # Sandman
        out = filter(img, Colors.PURPLE.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        positions = self.contours_to_location(contours)
        for position in positions:
            row, col = position
            self.arena[row][col] = 3

        # Electro
        out = filter(img, Colors.YELLOW.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        positions = self.contours_to_location(contours)
        for position in positions:
            row, col = position
            self.arena[row][col] = 2

        # Blocked Cell
        out = filter(img, Colors.WHITE.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        positions = self.contours_to_location(contours)
        for position in positions:
            row, col = position
            self.arena[row][col] = 1

        # Antidode
        out = filter(img, Colors.PINK.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        positions = self.contours_to_location(contours)
        for position in positions:
            row, col = position
            self.antidodes.append((row, col))

        # Spiderman
        out = filter(img, Colors.RED.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        positions = self.contours_to_location(contours)
        for position in positions:
            row, col = position
            self.spiderman.append((row, col))

        # Enemies position
        out = filter(img, Colors.VILLAN.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True).tolist()
            if len(approx) == 4:
                self.goblin[0] = self.contours_to_location([contour])[0]
            elif len(approx) == 3:
                self.sandman[0] = self.contours_to_location([contour])[0]
            else:
                self.electro[0] = self.contours_to_location([contour])[0]
            

    def revel_antidodes(self):
        '''
        After Moving to all the 3-Spidermans this function will store the location of enimies antidodes
        '''
        # Antidodes Position

        img = self.env.camera_feed()

        out = filter(img, Colors.PINK.value)
        cv2.imshow("antidode", out)
        contours, _ = cv2.findContours(out, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.025 * cv2.arcLength(contour, True), True).tolist()
            if len(approx) == 4:
                self.goblin[1] = self.contours_to_location([contour])[0]
            elif len(approx) == 8: # error
                self.sandman[1] = self.contours_to_location([contour])[0]
            else:
                self.electro[1] = self.contours_to_location([contour])[0]


    def get_location(self):
        '''
        Return the location of robot in the arena
        '''
        img = self.env.camera_feed()
        # img = cv2.imread("sample_arena_img.png")

        out = filter(img, Colors.WHITE.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True).tolist()
            if len(approx) == 4:
                return self.contours_to_location([contour])[0]
        
        raise Exception("Position Not found")

    def contours_to_location(self, contours):
        positions = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True).tolist()
            X = sorted([ a[0][0] for a in approx ])
            Y = sorted([ a[0][1] for a in approx ])
            center_x = X[0] + (X[-1] - X[0])//2
            center_y = Y[0] + (Y[-1] - Y[0])//2
            row = int( (center_y - self.y_pad) / self.hex_height )
            col = int( (center_x - self.x_pad) / self.hex_width )
            positions.append((row, col))
        return positions

    

if __name__ == "__main__":
    parent_path = os.path.dirname(os.getcwd())
    os.chdir(parent_path)
    env = gym.make("pixelate_arena-v0")
    perception = Perception(env)
    perception.scan_arena()
    env.unlock_antidotes()
    perception.revel_antidodes()
    print(perception.arena)
    print(perception.spiderman, perception.goblin, perception.sandman, perception.electro)

    cv2.waitKey(0)
    