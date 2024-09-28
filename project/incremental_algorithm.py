import matplotlib.pyplot as plt
import math
import random
import numpy as np

def sort_to_x(points):
   
    '''Sorts in ascending order based on x value 
        If equal sorts based on y value'''
   
    sorted_points = sorted(points, key=lambda k: [k[0], k[1]])
    return sorted_points    

# Calculates the orientation of three points 
# got this function from:
# https://www.geeksforgeeks.org/orientation-3-ordered-points/
def orientation(p, q, r):
    """Calculates the orientation of three points 
    Returns:
    0 -> p, q, r collinear
    1 -> (Clockwise)
    2 -> (Counterclockwise)
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2
    
def grahams_incremental_algorithm(points):
    
    #sort in ascending oreder based on x value
    sorted_points = sort_to_x(points)
    
    # Initialise L upper
    L_upper = [sorted_points[0], sorted_points[1]]
    
    for point in sorted_points[2:]:
        while len(L_upper) >= 2  and orientation(L_upper[-2], L_upper[-1], point) != 2:
            L_upper.pop(-1)
        L_upper.append(point)
    
    # Initialise L lower
    L_lower = [sorted_points[-1], sorted_points[-2]]
    for point in sorted_points[-3::-1]:
        
        while len(L_lower) >= 2  and orientation(L_lower[-2], L_lower[-1], point) != 2:
            L_lower.pop(-1)
        L_lower.append(point)
    #pop first and last element to avoid duplicates
    L_lower.pop(0)
    L_lower.pop()
    
    # merge
    L = L_upper + L_lower
    
    return L
        