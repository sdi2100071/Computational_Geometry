import sys 
import time
import random
import collections
from tabulate import tabulate
import matplotlib.pyplot as plt


def sort_to_x(points):
   
    '''Sorts in ascending order based on x value 
        If equal sorts based on y value'''
   
    sorted_points = sorted(points, key=lambda k: [k[0], k[1]])
    return sorted_points  


# https://www.geeksforgeeks.org/program-check-three-points-collinear/
def are_collinear(p1, p2, p3):
    """Check if three points are collinear."""
    
    # aka ((y3 - y2)*(x2 - x1) == (y2 - y1)*(x3 - x2))
    return (p3[1] - p2[1]) * (p2[0] - p1[0]) == (p2[1] - p1[1]) * (p3[0] - p2[0])


def generate_generic_points(num_points, x_range=(0, 100), y_range=(0, 100)):
   
    """Generates points in generic position"""
    points = []

    while len(points) < num_points:
        rand_point = (random.randint(0,100), random.randint(0, 100))

        # for each pair in points list check if its collinear with the new generated point
        collinear = False
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                if are_collinear(points[i], points[j], rand_point):
                    collinear = True
                    break
            if collinear:
                break

        if not collinear:
            points.append(rand_point)
    
    return points