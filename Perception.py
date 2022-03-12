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
        self.antidodes = [(0, 0), (0, 0), (0, 0)]  # Goblin, sandman, electro
        self.enemy = [(0, 0), (0, 0), (0, 0)]  # Goblin, sandman, electro

        # params
        self.y_pad = 60
        self.x_pad = 24
        self.hex_height = 45.5
        self.hex_width = 26

    def scan_arena(self):
        '''
        Decription of Arena:
        0 -> Empty Cell
        1 -> Spiderman
        2 -> Goblin
        3 -> Sandman
        4 -> Electro
        5 -> Antidode
        6 -> Blocked Cell
        '''
        img = self.env.camera_feed()
        # img = cv2.imread("sample_arena_img.png")

        # Goblin
        out = filter(img, Colors.GREEN.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        positions = self.contours_to_location(contours)
        for position in positions:
            row, col = position
            self.arena[row][col] = 2

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
            self.arena[row][col] = 4

        # Antidode
        out = filter(img, Colors.PINK.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        positions = self.contours_to_location(contours)
        for position in positions:
            row, col = position
            self.arena[row][col] = 5

        # Blocked Cell
        out = filter(img, Colors.WHITE.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        positions = self.contours_to_location(contours)
        for position in positions:
            row, col = position
            self.arena[row][col] = 6

        # Spiderman
        out = filter(img, Colors.RED.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        positions = self.contours_to_location(contours)
        for position in positions:
            row, col = position
            self.arena[row][col] = 1

        # Enemies position
        out = filter(img, Colors.VILLAN.value)
        contours, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True).tolist()
            if len(approx) == 4:
                self.enemy[0] = self.contours_to_location([contour])[0]
            elif len(approx) == 3:
                self.enemy[1] = self.contours_to_location([contour])[0]
            else:
                self.enemy[2] = self.contours_to_location([contour])[0]

        # Antidodes Position
        # out = self.filter(img, Colors.PINK.value)
        # cv2.imshow("antidodes", out)
        # contours, _ = cv2.findContours(out, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # for contour in contours:
        #     approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True).tolist()
        #     if len(approx) == 4:
        #         self.antidodes[0] = self.contours_to_location([contour])[0]
        #     elif len(approx) == 3:
        #         self.antidodes[1] = self.contours_to_location([contour])[0]
        #     else:
        #         self.antidodes[2] = self.contours_to_location([contour])[0]

        print("Arena : ")
        print_arena(self.arena)
        print(f"Antidodes location : {self.antidodes}")
        print(f"Enemies location : {self.enemy}")

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
    perception = Perception()
    perception.scan_arena()
    location = perception.get_location()
    print(f"Robot location : {location}")
    cv2.waitKey(0)
    