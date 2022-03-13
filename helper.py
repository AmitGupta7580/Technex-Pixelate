import cv2
import math
import numpy as np

def print_arena(arena):
    '''
    Funtion to display self.arena 
    '''
    for r in arena:
        for c in r:
            if c == 0:
                print("", end=" ")
            else:
                print(c, end="")
        print()

def filter(image, boundary):
    (lower, upper) = boundary
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(output, (0,0), sigmaX=33, sigmaY=33)
    output = cv2.divide(output, blur, scale=255)
    output = cv2.threshold(output, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    output = cv2.morphologyEx(output, cv2.MORPH_CLOSE, kernel)
    return output

def angle(point1, point2):
    if point1[1] == point2[1]:
        return 0.0
    return math.atan( ( point2[1] - point1[1] ) / ( point2[0] - point1[0] ) )

def dist(point1, point2):
    d = ( (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 )**(1/2)
    return d

if __name__ == "__main__":
    print("These are helper functions")