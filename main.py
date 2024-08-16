import incremental_algorithm 
import matplotlib.pyplot as plt
import random


if __name__ == "__main__":

    points = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(120)]
    
    hull = incremental_algorithm.grahams_incremental_algorithm(points)

    plt.figure()
    plt.scatter(*zip(*points), label="Σημεία")
    hull.append(hull[0])  # Κλείσιμο του κυρτού περιβλήματος
    plt.plot(*zip(*hull), 'r-', label="Κυρτό Περίβλημα")
    plt.legend()
    plt.show()