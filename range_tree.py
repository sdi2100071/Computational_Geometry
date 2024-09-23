import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
import time

# Step 1: Generate a random set of points with 2 decimal places
def create_points(num):
    np.random.seed(0)
    sample_cords = []
    for _ in range(num):
        x = round(random.random(), 2)
        y = round(random.random(), 2)
        sample_cords.append((x, y))
    return sample_cords

# Helper class for building the range tree
class TreeNode:
    def __init__(self, point=None, left=None, right=None, y_tree=None):
        self.point = point
        self.left = left
        self.right = right
        self.y_tree = y_tree

# Function to build a tree from y-sorted points
def build_y_tree(y_points):
    if not y_points:
        return None

    # Sort y_points by y-coordinate
    y_points.sort(key=lambda point: point[1])
    
    # Select median point
    median_idx = len(y_points) // 2
    median_point = y_points[median_idx]

    # Recursively construct left and right subtrees
    left_subtree = build_y_tree(y_points[:median_idx])
    right_subtree = build_y_tree(y_points[median_idx + 1:])
    
    return TreeNode(point=median_point, left=left_subtree, right=right_subtree)

# Step 2: Range tree construction
def build_range_tree(points):
    if not points:
        return None


    # Build the y-sorted points tree
    # y_tree_tree = build_y_tree(points)

    # Sort points by x-coordinate
    points.sort(key=lambda point: point[0])
    
    # Select median point
    median_idx = len(points) // 2
    median_point = points[median_idx]
    
    # Recursively construct left and right subtrees
    left_subtree = build_range_tree(points[:median_idx])
    right_subtree = build_range_tree(points[median_idx + 1:])
    y_tree_tree = build_y_tree(points)
    
    
    return TreeNode(point = median_point, left = left_subtree, right = right_subtree, y_tree = y_tree_tree)



# Find spkit node based on x coordinate.
def find_splitnode(range_tree, x_range):
    # Traverse the tree to find the split node based on the x_range.
    if range_tree is None:
        return
    
        # Assuming the node's point is a tuple (x, y)
    if range_tree.point[0] < x_range[0]:  # x < x_min
        find_splitnode(range_tree.right, x_range)
    if range_tree.point[0] > x_range[1]:  # x > x_max
        find_splitnode(range_tree.left, x_range)

    return range_tree  # Found the split node
    

def y_query(root, y_range, results):
    if root is None:
        return
    
    # Assuming node.point is (x, y)
    if y_range[0] <= root.point[1] <= y_range[1]:
        results.append(root.point)  # Report the point
    
    # Recur for left and right children
    if root.point[1] > y_range[0]:  # Check left subtree
        y_query(root.left, y_range, results)
    if root.point[1] < y_range[1]:  # Check right subtree
        y_query(root.right, y_range, results)

    return results


def valid_points(x_range, results):
    final_result = []
    for point in results:
        if point[0] >= x_range[0] and point[0] <= x_range[1]:
            final_result.append(point)

    return final_result


# Step 3: 2d range query.
def two_d_range_query(T, x_range, y_range):
    u_split = find_splitnode(T, x_range)
    results = []
    
    if u_split is None:
        return results  # No split node found.
    
    # If the split node is a leaf, report its point if within y_range.
    if u_split.left is None and u_split.right is None:
        if y_range[0] <= u_split.point[1] <= y_range[1]:
            results.append(u_split.point)

        return valid_points(x_range, results)

    
    # Otherwise, continue down the tree.
    results = y_query(u_split.y_tree, y_range, results)
    
    return valid_points(x_range, results)


# Step 4: Visualize Points and the Query Range.
def plot_points(points, rectangle=None, found_points=None):
    points = np.array(points)
    found_points = np.array(found_points) if found_points else []
    
    plt.scatter(points[:, 0], points[:, 1], label="Points", color='blue')

    if rectangle is None:
        return 
    
    if len(found_points) == 1:
        plt.scatter(found_points[0][0], found_points[0][1], label="Found Point", color='red')
    elif len(found_points) > 1:
        plt.scatter(found_points[:, 0], found_points[:, 1], label="Found Points", color='red')
    
    
    # Draw the rectangle.
    x1, x2, y1, y2 = rectangle
    plt.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], color='green', label="Query Range")
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()

def visualize_tree(root, ax, depth=0, x_pos=0.5, y_pos=1, x_offset=0.2, layer_factor=0.1, col='red'):
    if root is None:
        return
    
    # Draw the current node.
    ax.scatter(x_pos, y_pos, color=col, s=100)
    ax.annotate(f"{root.point}", (x_pos, y_pos), textcoords="offset points", xytext=(0,10), ha='center')

    # Recursively visualize left and right subtrees.
    if root.left:
        # Draw line to the left child.
        new_x_pos = x_pos - x_offset
        new_y_pos = y_pos - layer_factor  # Moving down in the tree.
        ax.plot([x_pos, new_x_pos], [y_pos, new_y_pos], color='black')
        visualize_tree(root.left, ax, depth + 1, new_x_pos, new_y_pos, x_offset * 0.5, layer_factor, col)

    if root.right:
        # Draw line to the right child.
        new_x_pos = x_pos + x_offset
        new_y_pos = y_pos - layer_factor  # Moving down in the tree.
        ax.plot([x_pos, new_x_pos], [y_pos, new_y_pos], color='black')
        visualize_tree(root.right, ax, depth + 1, new_x_pos, new_y_pos, x_offset * 0.5, layer_factor, col)

def visualize_range_tree_construction(points):
    range_tree = build_range_tree(points)

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    axs[0].set_title("X-Tree Construction")
    visualize_tree(range_tree, axs[0], x_pos=0.5, y_pos=1, x_offset=0.2, layer_factor=0.1, col = "blue")
    
    axs[1].set_title("Y-Tree Construction for Root Node")
    visualize_tree(range_tree.y_tree, axs[1], x_pos=0.05, y_pos=1, x_offset=0.2, layer_factor=0.1, col = "red")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    points = create_points(10)  
    visualize_range_tree_construction(points)
    
    n = 120
    points = create_points(n)

    # Step 2: Build the range tree
    range_tree = build_range_tree(points)
    
    # Step 3: Query the range tree
    x_range = (0.3, 0.7)
    y_range = (0.3, 0.7)

    found_points = two_d_range_query(range_tree, x_range, y_range)

    # Step 4: Visualize results
    rectangle = (x_range[0], x_range[1], y_range[0], y_range[1])
    plot_points(points, rectangle, found_points)

