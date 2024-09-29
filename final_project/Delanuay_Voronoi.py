import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d

class DelanuayAndVoronoi:
    
    def __init__(self, n_points):
        self.n_points = n_points
        self.points = self.generate_random_points()
    

    # Generate random points
    def generate_random_points(self):
        np.random.seed(0)
        rand_points = [(random.random(), random.random()) for _ in range(self.n_points)]
        return rand_points


    # Delaunay Triangulation
    def delaunay_triangulation(self):
        delaunay = Delaunay(self.points)
        return np.array(self.points), delaunay.simplices

    # Plot Delaunay
    def plot_delaunay(self, ax, points, simplices):
        
        ax.scatter(points[:, 0], points[:, 1], c='r', zorder=2)
        for simplex in simplices:
            for idx in range(len(simplex)):
                start_idx, end_idx = simplex[idx], simplex[(idx + 1) % len(simplex)]
                ax.plot([points[start_idx, 0], points[end_idx, 0]], 
                        [points[start_idx, 1], points[end_idx, 1]], 'k-', zorder=1)
        
        ax.set_title("Delaunay Triangulation")
        ax.set_aspect('equal')


    # Voronoi diagram
    def plot_voronoi(self, ax, vor):
        
        voronoi_plot_2d(vor, ax=ax, show_vertices=False, 
                        line_colors='blue', line_width=1.5, zorder=1)
        
        ax.scatter(*zip(*self.points), color='r', s=50, edgecolor='black', zorder=2)
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_title("Voronoi Diagram")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_aspect('equal')

    # Plot Delaunay and Voronoi diagrams
    def plot_both(self):
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        
        # Delaunay Triangulation
        current_points, simplices = self.delaunay_triangulation()
        self.plot_delaunay(ax1, current_points, simplices)

        # Voronoi Diagram
        vor = Voronoi(self.points)
        self.plot_voronoi(ax2, vor)

        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
   
    # Set number of points
    points_num = 10
    tv = DelanuayAndVoronoi(points_num)
    
    # Plot Delaunay and Voronoi
    tv.plot_both()
