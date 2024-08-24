import matplotlib.pyplot as plt
import random

def distance_from_line(point, line_start, line_end):

    return abs((line_end[1] - line_start[1]) * point[0] - (line_end[0] - line_start[0]) * point[1] + line_end[0] * line_start[1] - line_end[1] * line_start[0]) / ((line_end[1] - line_start[1]) ** 2 + (line_end[0] - line_start[0]) ** 2) ** 0.5

def is_point_right_of_line(point, line_start, line_end):

    return (line_end[0] - line_start[0]) * (point[1] - line_start[1]) - (line_end[1] - line_start[1]) * (point[0] - line_start[0]) > 0


def quickhull(points):

    # find the extreme points
    min_x_point = min(points, key=lambda p: p[0])
    max_x_point = max(points, key=lambda p: p[0])
    min_y_point = min(points, key=lambda p: p[1])
    max_y_point = max(points, key=lambda p: p[1])

    # Initial set of points to ignore those inside the quadrilateral
    initial_hull = [min_x_point, max_x_point, min_y_point, max_y_point]

    # Remove initial hull points from points set
    remaining_points = [p for p in points if p not in initial_hull]

    # Separate points into four regions
    region_1 = [p for p in remaining_points if is_point_right_of_line(p, min_x_point, max_y_point)]
    region_2 = [p for p in remaining_points if is_point_right_of_line(p, max_y_point, max_x_point)]
    region_3 = [p for p in remaining_points if is_point_right_of_line(p, max_x_point, min_y_point)]
    region_4 = [p for p in remaining_points if is_point_right_of_line(p, min_y_point, min_x_point)]

    # Apply QuickHull recursively on each region
    upper_hull = quickhull_rec(region_1, min_x_point, max_y_point) + quickhull_rec(region_2, max_y_point, max_x_point)
    lower_hull = quickhull_rec(region_3, max_x_point, min_y_point) + quickhull_rec(region_4, min_y_point, min_x_point)

    return upper_hull + lower_hull

def quickhull_rec(points, line_start, line_end):
    """Recursive function for QuickHull algorithm."""
    if not points:
        return [line_start]

    # Find point C with the maximum distance from line segment AB
    point_C = max(points, key=lambda p: distance_from_line(p, line_start, line_end))

    # Points to the right of AC and CB
    M = [point for point in points if is_point_right_of_line(point, line_start, point_C)]
    N = [point for point in points if is_point_right_of_line(point, point_C, line_end)]

    # Recursive search on both segments
    return quickhull_rec(M, line_start, point_C) + quickhull_rec(N, point_C, line_end)

# Example usage
# if __name__ == "__main__":
#     # Generate 120 random points
#     random_points = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(120)]

#     # Find the convex hull
#     convex_hull = quickhull(random_points)
    
#     # Plot points and convex hull
#     plt.figure(figsize=(8, 8))
#     plt.scatter(*zip(*random_points), label="Points")
#     convex_hull.append(convex_hull[0])  # To close the convex hull loop
#     plt.plot(*zip(*convex_hull), 'r-', label="Convex Hull")
#     plt.title("QuickHull Convex Hull")
#     plt.legend()
#     plt.show()
