
import matplotlib.pyplot as plt
import random
import sys 
from convex_hull_alg import Convex_Hull 
import time

def sort_to_x(points):
   
    '''Sorts in ascending order based on x value 
        If equal sorts based on y value'''
   
    sorted_points = sorted(points, key=lambda k: [k[0], k[1]])
    return sorted_points  


def are_collinear(p1, p2, p3):
    """ check if three points are collinear."""
    return (p3[1] - p2[1]) * (p2[0] - p1[0]) == (p2[1] - p1[1]) * (p3[0] - p2[0])

def generate_generic_points(num_points):
    """Generate points in generic position (no three points are collinear)."""
    points = []

    while len(points) < num_points:
        rand_point = (random.randint(0, 100), random.randint(0, 100))

        # Check if the new point is collinear with any two existing points
        collinear = False
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                if are_collinear(points[i], points[j], rand_point):
                    collinear = True
                    break
            if collinear:
                break

        # If not collinear, add the point
        if not collinear:
            points.append(rand_point)
    
    return points


# not complete

# def benchmark_convex_hull_algorithms(algo):
#     """Benchmark convex hull algorithms with increasing number of points."""
#     num_points_list = [10, 50, 100, 500, 1000, 5000, 10000]
#     algorithms = {'Graham Scan': algo.grahams, 'QuickHull': quickhull, 'Divide and Conquer': divide_and_conquer}
#     results = {name: [] for name in algorithms}

#     for num_points in num_points_list:
#         points = generate_generic_points(num_points)
#         print(f"\nTesting with {num_points} points:")
#         for name, algorithm in algorithms.items():
#             start_time = time.time()
#             hull = algorithm(points)
#             elapsed_time = time.time() - start_time
#             results[name].append(elapsed_time)
#             print(f"{name}: {elapsed_time:.6f} seconds")

#     # Plotting the results
#     plt.figure(figsize=(10, 6))
#     for name, times in results.items():
#         plt.plot(num_points_list, times, label=name)
#     plt.xlabel('Number of Points')
#     plt.ylabel('Time (seconds)')
#     plt.title('Convex Hull Algorithms Performance')
#     plt.legend()
#     plt.grid(True)
#     plt.show()


if __name__ == "__main__":
    
    # generate 120 random points in generic position
    points = generate_generic_points(120)  
    
    # sort based on x
    sorted_points = sort_to_x(points)
    # print(sorted_points)
    
    # initialise object
    algo = Convex_Hull(sorted_points)
    
    
    hull = algo.grahams_incremental(points, algo)
    
    algo.plot(points, hull)
    
    
    # # hull = jarvis_march_algorithm.jarvis_march(sorted_points)
    # # hull = divide_and_conquer_algorithm.divide_and_conquer(sorted_points)
    # hull = quick_hull_algorithm.quickhull(sorted_points)
    
    # plt.figure()
    # plt.scatter(*zip(*points), label="Σημεία")
    # hull.append(hull[0])  # Κλείσιμο του κυρτού περιβλήματος
    # plt.plot(*zip(*hull), 'r-', label="Κυρτό Περίβλημα")
    # plt.legend()
    # plt.show()
    
    