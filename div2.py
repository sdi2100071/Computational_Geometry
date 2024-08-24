import matplotlib.pyplot as plt
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cw_next = None
        self.ccw_next = None

    def subtract(self, p):
        return Point(self.x - p.x, self.y - p.y)

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

def merge_hulls(chull1, chull2):
    # get the rightmost point of left convex hull
    p = max(chull1, key = lambda point: chull1[0])

    # get the leftmost poitn of right convex hull
    q = min(chull2, key = lambda point: chull2[0])

    # make copies of p and q
    cp_p = p
    cp_q = q

    # raise the bridge pq to the uper tangent
    prev_p = None
    prev_q = None
    while (True):
        prev_p = p
        prev_q = q
        if q.cw_next:
            # move p clockwise as long as it makes left turn
            while orientation(p, q, q.cw_next) < 0:
                q = q.cw_next
        if p.ccw_next:
            # move p as long as it makes right turn
            while orientation(q, p, p.ccw_next) > 0:
                p = p.ccw_next

        if p == prev_p and q == prev_q:
            break
    
    # lower the bridge cp_p cp_q to the lower tangent
    prev_p = None
    prev_q = None
    while (True):
        prev_p = cp_p
        prev_q = cp_q
        if cp_q.ccw_next:
            # move q as long as it makes right turn
            while orientation(cp_p, cp_q, cp_q.ccw_next) > 0:
                cp_q = cp_q.ccw_next
        if cp_p.cw_next:
            # move p as long as it makes left turn
            while orientation(cp_q, cp_p, cp_p.cw_next) < 0:
                cp_p = cp_p.cw_next
        if cp_p == prev_p and cp_q == prev_q:
            break

    # remove all other points
    p.cw_next = q
    q.ccw_next = p

    cp_p.ccw_next = cp_q
    cp_q.cw_next = cp_p

    # final result
    result = []
    start = p 
    while (True):
        result.append(p)
        p = p.ccw_next

        if p == start:
            break

    return result


def orientation(p, q, r):
    """Calculates the orientation of the triplet (p, q, r).
    Returns:
    0 -> p, q, r are collinear
    1 -> Clockwise
    2 -> Counterclockwise
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


def sort_to_x(points):
   
    '''Sorts in ascending order based on x value 
        If equal sorts based on y value'''
   
    sorted_points = sorted(points, key=lambda k: [k[0], k[1]])
    return sorted_points  


def find_upper_bridge(A, B):
    """Finds the upper bridge (tangent) between two convex hulls A and B."""
    # Step 1: Initialize Ai and Bj
    # print(A)
    # print(max(A, key=lambda x: (x[0], x[1])))
    i = A.index(max(A, key=lambda x: (x[0], x[1]))) # Rightmost point of A
    j = B.index(min(B, key=lambda x: (x[0], x[1])))           # Leftmost point of B
    
    # Step 2-4: Adjust i and j to find the upper tangent
    while True:
        moved = False

        # Check if the line Ai, Ai+1 is not an upper tangent
        while orientation(A[i], B[j], A[(i + 1) % len(A)]) == 2:
            i = (i + 1) % len(A)
            moved = True
        
        # Check if the line Bj, Bj-1 is not an upper tangent
        while orientation(B[j], A[i], B[(j - 1) % len(B)]) == 1:
            j = (j - 1) % len(B)
            moved = True
        
        # If neither i nor j has moved, we have found the upper tangent
        if not moved:
            break

    # Return the indices of the upper tangent points Ai and Bj
    return i, j

# def merge_hulls(A, B):
#     """Merges two convex hulls A and B using the upper and lower bridges."""
#     # Find upper tangent
#     upper_i, upper_j = find_upper_bridge(A, B)
    
#     # Find lower tangent
#     lower_i, lower_j = find_upper_bridge(A[::-1], B[::-1])
#     lower_i = len(A) - 1 - lower_i
#     lower_j = len(B) - 1 - lower_j

#     # Merge convex hulls using the upper and lower tangents
#     merged_hull = []

#     # Add points from A starting from upper_i to lower_i
#     index = upper_i
#     while True:
#         merged_hull.append(A[index])
#         if index == lower_i:
#             break
#         index = (index + 1) % len(A)
    
#     # Add points from B starting from lower_j to upper_j
#     index = lower_j
#     while True:
#         merged_hull.append(B[index])
#         if index == upper_j:
#             break
#         index = (index + 1) % len(B)

#     return merged_hull



def divide_and_conquer(points):
   
    """Divide and conquer algorithm to find the convex hull."""
    
    if len(points) <= 3:
        # Sort and remove collinear points if there are exactly 3 points
        points = sort_to_x(points)
        if len(points) == 3 and orientation(points[0], points[1], points[2]) == 0:
            points.pop(1)
        return points

    mid = len(points) // 2
    left_hull = divide_and_conquer(points[:mid])
    right_hull = divide_and_conquer(points[mid:])

    return merge_hulls(left_hull, right_hull)

