import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy.spatial import Voronoi, voronoi_plot_2d

def create_points(num):
    np.random.seed(0)
    sample_cords = []
    for _ in range(num):
        sample_cords.append((random.random(), random.random()))
    return sample_cords


     
