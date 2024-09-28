import matplotlib.pyplot as plt
import numpy as np


class Convex_Hull:
    
    '''
   
    Contains the the implementations of the various algorithms for
    calculating the convex hull (2D) along with the needed additional
    functions
   
    '''
    
    def __init__(self, points):
       
        ''''
        
        Initialise with given input of (x,y) points and sort based on x
        
        '''
        self.points = sorted(points, key = lambda x: x[0]) 
    
    
    def plot(points, convex_hull, algorithm_name):
       
        '''
        Creates a plot for a fiven convex hull and the points 
        '''
        
        plt.figure()
        plt.scatter(*zip(*points), label="Points")
        convex_hull.append(convex_hull[0]) 
        plt.plot(*zip(*convex_hull), 'r-', label="Convex_Hull")
        plt.title(algorithm_name)
        plt.legend()
        plt.show()
    
    
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
        
        
    def distance(p1, p2):
        '''
        Calculates Eucledean Distance between two given points
        '''
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    
                
    def grahams_incremental(points, self):
        
        # Initialise L upper
        L_upper = [points[0],points[1]]
        
        for point in points[2:]:
            while len(L_upper) >= 2  and self.orientation(L_upper[-2], L_upper[-1], point) != 2:
                L_upper.pop(-1)
            L_upper.append(point)
        
        # Initialise L lower
        L_lower = [points[-1], points[-2]]
        for point in points[-3::-1]:
            
            while len(L_lower) >= 2  and self.orientation(L_lower[-2], L_lower[-1], point) != 2:
                L_lower.pop(-1)
            L_lower.append(point)
        #pop first and last element to avoid duplicates
        L_lower.pop(0)
        L_lower.pop()
        
        # merge
        L = L_upper + L_lower
        
        return L
        

    def jarvis_march(points, self):
        
        # find most left point 
        r0 = min(points, key=lambda p: p[0])
        
        L = []
        r = r0
        
        while True:
            
            L.append(r)
            u = points[0]
            
            for t in points:
                if self.orientation(r, u, t) == 2 or self.orientation(r, u, t) == 0 and self.distance(r, t) > self.distance(r, u):
                    u = t

            if u == r0:
                break
            
            r = u
            
        return L
    
    
    def merge_hulls(left_hull, right_hull, self):
        
        n1, n2 = len(left_hull), len(right_hull)
        
        i = max(range(n1), key=lambda x: left_hull[x][0])
        
        j = min(range(n2), key=lambda x: right_hull[x][0])

        upper_i, upper_j = i, j
        while True:
            moved = False
            while self.orientation(left_hull[upper_i], right_hull[upper_j], right_hull[(upper_j - 1) % n2]) == 2:
                upper_j = (upper_j - 1) % n2
                moved = True
            while self.orientation(right_hull[upper_j], left_hull[upper_i], left_hull[(upper_i + 1) % n1]) == 1:
                upper_i = (upper_i + 1) % n1
                moved = True
            if not moved:
                break

        lower_i, lower_j = i, j
        while True:
            moved = False
            while self.orientation(left_hull[lower_i], right_hull[lower_j], right_hull[(lower_j + 1) % n2]) == 1:
                lower_j = (lower_j + 1) % n2
                moved = True
            while self.orientation(right_hull[lower_j], left_hull[lower_i], left_hull[(lower_i - 1) % n1]) == 2:
                lower_i = (lower_i - 1) % n1
                moved = True
            if not moved:
                break

        merged_hull = []

        index = upper_i
        while index != lower_i:
            merged_hull.append(left_hull[index])
            index = (index + 1) % n1
        merged_hull.append(left_hull[lower_i])

        index = lower_j
        while index != upper_j:
            merged_hull.append(right_hull[index])
            index = (index + 1) % n2
        merged_hull.append(right_hull[upper_j])

        return merged_hull

    def divide_and_conquer(points, self):
        
        if len(points) <= 3:
            return points

        mid = len(points) // 2
        left_hull = self.divide_and_conquer(points[:mid],self)
        right_hull = self.divide_and_conquer(points[mid:], self)

        return self.merge_hulls(left_hull, right_hull, self)
    
    
    
    def distance_from_line(point, line_start, line_end):

        return abs((line_end[1] - line_start[1]) * point[0] - (line_end[0] - line_start[0]) * point[1] + line_end[0] * line_start[1] - line_end[1] * line_start[0]) / ((line_end[1] - line_start[1]) ** 2 + (line_end[0] - line_start[0]) ** 2) ** 0.5

    def is_point_right_of_line(point, line_start, line_end):

        return (line_end[0] - line_start[0]) * (point[1] - line_start[1]) - (line_end[1] - line_start[1]) * (point[0] - line_start[0]) > 0


    def quickhull(points, self):

        # find the extreme points
        min_x_point = min(points, key=lambda p: p[0])
        max_x_point = max(points, key=lambda p: p[0])
        min_y_point = min(points, key=lambda p: p[1])
        max_y_point = max(points, key=lambda p: p[1])

        initial_hull = [min_x_point, max_x_point, min_y_point, max_y_point]

        remaining_points = [p for p in points if p not in initial_hull]

        region_1 = [p for p in remaining_points if self.is_point_right_of_line(p, min_x_point, max_y_point)]
        region_2 = [p for p in remaining_points if self.is_point_right_of_line(p, max_y_point, max_x_point)]
        region_3 = [p for p in remaining_points if self.is_point_right_of_line(p, max_x_point, min_y_point)]
        region_4 = [p for p in remaining_points if self.is_point_right_of_line(p, min_y_point, min_x_point)]

        upper_hull = self.quickhull_rec(region_1, min_x_point, max_y_point, self) + self.quickhull_rec(region_2, max_y_point, max_x_point, self)
        lower_hull = self.quickhull_rec(region_3, max_x_point, min_y_point, self) + self.quickhull_rec(region_4, min_y_point, min_x_point, self)

        return upper_hull + lower_hull

    def quickhull_rec(points, line_start, line_end, self):
       
        if not points:
            return [line_start]

        point_C = max(points, key=lambda p: self.distance_from_line(p, line_start, line_end))

        M = [point for point in points if self.is_point_right_of_line(point, line_start, point_C)]
        N = [point for point in points if self.is_point_right_of_line(point, point_C, line_end)]

        return self.quickhull_rec(M, line_start, point_C, self) + self.quickhull_rec(N, point_C, line_end, self)


    
                
        
