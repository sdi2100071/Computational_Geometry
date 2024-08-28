import numpy as np
from scipy.optimize import linprog

def incremental_algorithm(c, A, b):
    """
    Incremental Algorithm for Linear Programming
    :param c: Coefficients of the objective function (for minimization)
    :param A: Coefficients of the constraints
    :param b: Right-hand side of the constraints
    :return: Optimal solution or "Infeasible"
    """

    d = len(c)  # Number of variables

    # Step 1: Initialize with d+1 constraints to find an initial feasible solution
    if len(A) < d + 1:
        print("Infeasible")
        return
    
    # Define the initial problem with d+1 constraints
    A_initial = A[:d+1]
    b_initial = b[:d+1]
    
    # Solve initial problem
    res = linprog(c, A_ub=A_initial, b_ub=b_initial, method='highs')
    if res.success:
        x_current = res.x
    else:
        print("Infeasible")
        return

    # Step 2: Incrementally add constraints
    for i in range(d+1, len(A)):
        A_new = A[:i+1]
        b_new = b[:i+1]
        
        # Check if the current solution satisfies the new constraint
        if np.dot(A[i], x_current) <= b[i]:
            continue  # Current solution is feasible for this constraint
        
        # Solve the problem with the new constraint
        A_new = np.array(A_new)
        b_new = np.array(b_new)
        
        res = linprog(c, A_ub=A_new, b_ub=b_new, method='highs')
        if res.success:
            x_current = res.x
        else:
            print("Infeasible")
            return

    print("Optimal Solution Found:", x_current)
    return x_current

# Example Usage
c = [1, 2]  # Objective function coefficients
A = [
    [1, 1],
    [1, -1],
    [-1, 0],
    [0, -1]
]
b = [2, 1, 0, 0]  # Right-hand side of constraints

incremental_algorithm(c, A, b)
