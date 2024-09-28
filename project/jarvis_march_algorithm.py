import matplotlib.pyplot as plt


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
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def jarvis_march(points):
    
    # find most left point 
    r0 = min(points, key=lambda p: p[0])
    
    L = []
    r = r0
    
    while True:
        
        L.append(r)
        u = points[0]
        
        for t in points:
            if orientation(r, u, t) == 2 or orientation(r, u, t) == 0 and distance(r, t) > distance(r, u):
                u = t

        if u == r0:
            break
        
        r = u
        
    return L
            
    