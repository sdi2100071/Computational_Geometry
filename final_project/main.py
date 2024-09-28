import sys 
import time
import random
import collections
from tabulate import tabulate
import matplotlib.pyplot as plt

import point_operations
from ConvexHull import Convex_Hull 


if __name__ == "__main__":

#1
    # Generate set of random points in generic position
    points = point_operations.generate_generic_points(120)     
    sorted_points = point_operations.sort_to_x(points)
    
    
    # algorithms list
    convex_hull_algorithms = {"grahams_incremental": Convex_Hull.grahams_incremental, "jarvis_march" : Convex_Hull.jarvis_march,    
                                "divide_and_conquer": Convex_Hull.divide_and_conquer, "quickhull": Convex_Hull.quickhull}
    
    # 1.2     

    #
    
    alg = Convex_Hull(points)
    hull_list = []
    for name in convex_hull_algorithms.keys():
        
        hull = convex_hull_algorithms[name](sorted_points, Convex_Hull)
        hull_list.append(hull)
        Convex_Hull.plot(points, hull, name)

    # check if there are differences in the results of each algorithm
    # print False if not equal / True if equal

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
        sorted_points = point_operations.sort_to_x(points)
        time_list = []
        for name in convex_hull_algorithms.keys():
            
            start_time = time.time()
            hull = convex_hull_algorithms[name](sorted_points, Convex_Hull)
            end_time = time.time()
            
            time_list.append(end_time - start_time)
        
        duration_dict[num_points] = time_list  
    
        
    print(tabulate(duration_dict, headers="keys", tablefmt="fancy_grid"))

#2




