import matplotlib.pyplot as plt
import random
import collections
from convex_hull import Convex_Hull as algo
import time
from tabulate import tabulate
import sys 


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

if __name__ == "__main__":

#1
    # Generate set of random points in generic position
    points = generate_generic_points(120)     
    # points = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(500)]
    sorted_points = sort_to_x(points)
    
    
    # algorithms list
    convex_hull_algorithms = { "grahams_incremental": algo.grahams_incremental, "jarvis_march" : algo.jarvis_march,    
                                "divide_and_conquer": algo.divide_and_conquer, "quickhull": algo.quickhull}
    
    # 1.2     
    
    alg = algo(points)
    hull_list = []
    for name in convex_hull_algorithms.keys():
        
        hull = convex_hull_algorithms[name](sorted_points, algo)
        hull_list.append(hull)
        algo.plot(points, hull, name)

    # check if there are differences in the results of each algorithm
    # print False if not equal / True if equal
    # ---> !! divide and conq is not equal to the rest !!
    print("Checking for differences........")
    print()
    compare = lambda a, b, c, d: collections.Counter(a) == collections.Counter(b) == collections.Counter(c) == collections.Counter(d)  

    different = compare(hull_list[0], hull_list[1], hull_list[2], hull_list[3])
    if different:
        print("There are differences in the results of the algorithms")
        print()
    else:
        print("There are no differences in the results of the algorithms. They are the same.")
        print()

    
    # 1.3
    
    num_points_list = [50, 120, 500, 1000, 100000]  
    
    
    duration_dict = {}
    duration_dict["number of points"] = convex_hull_algorithms.keys()
    for num_points in num_points_list:
        
        # Generate set of random points in generic position
        points = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_points)]
        sorted_points = sort_to_x(points)
        time_list = []
        for name in convex_hull_algorithms.keys():
            
            start_time = time.time()
            hull = convex_hull_algorithms[name](sorted_points, algo)
            end_time = time.time()
            
            time_list.append(end_time - start_time)
        
        duration_dict[num_points] = time_list  
        
    print(tabulate(duration_dict, headers="keys", tablefmt="fancy_grid"))

#2






            
                    
        
        
        
    
    
    
    
    
    
