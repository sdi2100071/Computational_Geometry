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
    
    # Divide and Conquer

    def merge_hulls(left_hull, right_hull, self):
        
        # number of points for each hull
        n1, n2 = len(left_hull), len(right_hull)
        
        # initialise with most left and most right
        lefter = max(range(n1), key=lambda x: left_hull[x][0])
        righter = min(range(n2), key=lambda x: right_hull[x][0])


        # Find upper hull
        lefter_up, righter_up = lefter, righter
        while True:
            moved = False
            while self.orientation(left_hull[lefter_up], right_hull[righter_up], right_hull[(righter_up - 1) % n2]) == 2:
                righter_up = (righter_up - 1) % n2
                moved = True
            while self.orientation(right_hull[righter_up], left_hull[lefter_up], left_hull[(lefter_up + 1) % n1]) == 1:
                lefter_up = (lefter_up + 1) % n1
                moved = True
            if not moved:
                break

        # Find lower hull
        lefter_down, righter_down = lefter, righter
        while True:
            moved = False
            while self.orientation(left_hull[lefter_down], right_hull[righter_down], right_hull[(righter_down + 1) % n2]) == 1:
                righter_down = (righter_down + 1) % n2
                moved = True
            while self.orientation(right_hull[righter_down], left_hull[lefter_down], left_hull[(lefter_down - 1) % n1]) == 2:
                lefter_down = (lefter_down - 1) % n1
                moved = True
            if not moved:
                break


        # Merge hulls
        merged_hull = []

        index = lefter_up
        while index != lefter_down:
            merged_hull.append(left_hull[index])
            index = (index + 1) % n1
        merged_hull.append(left_hull[lefter_down])

        index = righter_down
        while index != righter_up:
            merged_hull.append(right_hull[index])
            index = (index + 1) % n2
        merged_hull.append(right_hull[righter_up])

        return merged_hull

    def divide_and_conquer(points, self):
        
        # base case (recurse stops if <=3 points are left)
        if len(points) <= 3:
            return points

        # divide set of points in 2 subsets
        mid = len(points) // 2
        left_hull = self.divide_and_conquer(points[:mid],self)
        right_hull = self.divide_and_conquer(points[mid:], self)

        return self.merge_hulls(left_hull, right_hull, self)
    
    # Quick Hull
    
    #https://www.w3resource.com/python-exercises/python-basic-exercise-40.php
    def distance_from_line(point, line_start, line_end):

        return abs((line_end[1] - line_start[1]) * point[0] - (line_end[0] - line_start[0]) * point[1] + line_end[0] * line_start[1] - line_end[1] * line_start[0]) / ((line_end[1] - line_start[1]) ** 2 + (line_end[0] - line_start[0]) ** 2) ** 0.5

    def is_point_right_of_line(point, line_start, line_end):

        return (line_end[0] - line_start[0]) * (point[1] - line_start[1]) - (line_end[1] - line_start[1]) * (point[0] - line_start[0]) > 0


    def quickhull(points, self):

        # find the extreme points
        A = min(points, key=lambda p: p[0])
        B = max(points, key=lambda p: p[0])
        C = min(points, key=lambda p: p[1])
        D = max(points, key=lambda p: p[1])

        initial_hull = [A, B, C, D]
        remaining_points = [p for p in points if p not in initial_hull]

        AD = [p for p in remaining_points if self.is_point_right_of_line(p, A, D)]
        DB = [p for p in remaining_points if self.is_point_right_of_line(p, D, B)]
        BC = [p for p in remaining_points if self.is_point_right_of_line(p, B, C)]
        CA = [p for p in remaining_points if self.is_point_right_of_line(p, C, A)]

        upper_hull = self.quickhull_rec(AD, A, D, self) + self.quickhull_rec(DB, D, B, self)
        lower_hull = self.quickhull_rec(BC, B, C, self) + self.quickhull_rec(CA, C, A, self)

        return upper_hull + lower_hull

    def quickhull_rec(points, A, B, self):
       
        if not points:
            return [A]

        # point with max distance from line AB
        C = max(points, key=lambda p: self.distance_from_line(p, A, B))

        # points left AC
        M = [point for point in points if self.is_point_right_of_line(point, A, C)]

        # points on the right of CB 
        N = [point for point in points if self.is_point_right_of_line(point, C, B)]

        return self.quickhull_rec(M, A, C, self) + self.quickhull_rec(N, C, B, self)


    
                
        