import matplotlib.pyplot as plt
import random

def orientation(p, q, r):
    """Υπολογίζει τον προσανατολισμό των σημείων p, q, r.
    Επιστρέφει:
    0 -> p, q, r είναι συνευθειακά
    1 -> Δεξιόστροφα (Clockwise)
    2 -> Αριστερόστροφα (Counterclockwise)
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2

def merge_hulls(left_hull, right_hull):
    """Συνδυάζει τα δύο κυρτά περιβλήματα σε ένα."""
    
    n1, n2 = len(left_hull), len(right_hull)
    
    # Βρείτε το δεξιότερο σημείο του αριστερού περιβλήματος
    i = max(range(n1), key=lambda x: left_hull[x][0])
    
    # Βρείτε το αριστερότερο σημείο του δεξιού περιβλήματος
    j = min(range(n2), key=lambda x: right_hull[x][0])

    # Βρείτε την άνω συνένωση
    upper_i, upper_j = i, j
    while True:
        moved = False
        while orientation(left_hull[upper_i], right_hull[upper_j], right_hull[(upper_j - 1) % n2]) == 2:
            upper_j = (upper_j - 1) % n2
            moved = True
        while orientation(right_hull[upper_j], left_hull[upper_i], left_hull[(upper_i + 1) % n1]) == 1:
            upper_i = (upper_i + 1) % n1
            moved = True
        if not moved:
            break

    # Βρείτε την κάτω συνένωση
    lower_i, lower_j = i, j
    while True:
        moved = False
        while orientation(left_hull[lower_i], right_hull[lower_j], right_hull[(lower_j + 1) % n2]) == 1:
            lower_j = (lower_j + 1) % n2
            moved = True
        while orientation(right_hull[lower_j], left_hull[lower_i], left_hull[(lower_i - 1) % n1]) == 2:
            lower_i = (lower_i - 1) % n1
            moved = True
        if not moved:
            break

    # Συνδυασμός των δύο περιβλημάτων
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

def divide_and_conquer(points):
    """Διαίρει και βασίλευε για εύρεση κυρτού περιβλήματος."""
    
    if len(points) <= 3:
        # Ταξινόμηση και αφαίρεση συνευθειακών σημείων
        # points = sorted(points, key=lambda p: (p[0], p[1]))
        # if len(points) == 3 and orientation(points[0], points[1], points[2]) == 0:
        #     points.pop(1)
        return points

    mid = len(points) // 2
    left_hull = divide_and_conquer(points[:mid])
    right_hull = divide_and_conquer(points[mid:])

    return merge_hulls(left_hull, right_hull)

# # Παράδειγμα χρήσης:
# if __name__ == "__main__":
#     # Δημιουργία τυχαίων σημείων
#     points = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(20)]
    
#     # Ταξινόμηση των σημείων με βάση την x-συντεταγμένη
#     points = sorted(points, key=lambda p: p[0])

#     # Εύρεση του κυρτού περιβλήματος χρησιμοποιώντας τον αλγόριθμο "Διαίρει και Βασίλευε"
#     hull = divide_and_conquer(points)
    
#     # Σχεδίαση των σημείων και του κυρτού περιβλήματος
#     plt.figure(figsize=(8, 8))
#     plt.scatter(*zip(*points), label="Σημεία")
#     hull.append(hull[0])  # Κλείσιμο του κυρτού περιβλήματος
#     plt.plot(*zip(*hull), 'r-', label="Κυρτό Περίβλημα")
#     plt.legend()
#     plt.show()
