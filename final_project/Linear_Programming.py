import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from intvalpy import lineqs


def partial_solution(c, A, b):
    
    # Solve for the optimal solution under the given constraints
    result = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method='highs')
    
    # If the solution is valid and successful
    if result.success:
        return result.x, -result.fun
    return None, None


# Returns x_opt and f_opt for a new set of constraints.
def new_solution(constraints, H_new, x_opt):

    # Check if x_opt satisfies the latest constraint (H_new)
    if np.dot(H_new[:2], x_opt) <= H_new[2]:
        return x_opt, -np.dot(c, x_opt)
    
    # If x_opt violates the new constraint, reformulate and solve a new problem
    A = np.array([c[:2] for c in constraints])
    b = np.array([c[2] for c in constraints])
    
    # Adjust the constraint set with the new constraint
    updated_constraints = []
    for i in range(len(A)):
        constraint_diff = [
            A[i][0] - H_new[0], 
            A[i][1] - H_new[1], 
            b[i] - H_new[2]
        ]
        updated_constraints.append(constraint_diff)

    A_updated = np.array([constraint[:2] for constraint in updated_constraints])
    b_updated = np.array([constraint[2] for constraint in updated_constraints])
    
    # Solve the reformulated problem
    return partial_solution(c, A_updated, b_updated)


def incremental_algorithm(c, H_starting, H_rest):
   
    # Build the initial constraint matrix A and vector b from H_starting
    A = [constraint[:2] for constraint in H_starting]  
    b = [constraint[2] for constraint in H_starting]   

    # Find the optimal solution for the initial constraints
    x_opt, f_opt = partial_solution(c, A, b)
    
    # If no solution exists, terminate early
    if x_opt is None:
        return
    
    # Iterate through remaining constraints in H_rest
    for _, H_new in enumerate(H_rest, start=1):
        x_opt, f_opt = new_solution(H_starting, H_new, x_opt)
        
        # If no valid solution can be found, terminate
        if x_opt is None:
            return
        
        # Append the newly satisfied constraint to the set
        H_starting.append(H_new)
        
    # Return the final optimal solution
    return x_opt, f_opt


#https://stackoverflow.com/questions/57017444/how-to-visualize-feasible-region-for-linear-programming-with-arbitrary-inequali/57017638#57017638

# plot the feasible region
def plot_feasible_region(A, b, x_bounds, y_bounds):
   
    # generate a grid of x and y values
    x = np.linspace(x_bounds[0], x_bounds[1], 400)
    y = np.linspace(y_bounds[0], y_bounds[1], 400)
    x_grid, y_grid = np.meshgrid(x, y)

    region = np.ones_like(x_grid, dtype=bool)

    for i in range(8):
        # For constraint Ax + By <= b, we need to check if A[i][0]*x + A[i][1]*y <= b[i]
        region &= (A[i][0] * x_grid + A[i][1] * y_grid <= b[i])

    # Plot each constraint line
    for i in range(8):
        if A[i][1] != 0:
            y_line = (b[i] - A[i][0] * x) / A[i][1]
            plt.plot(x, y_line, label=f'{A[i][0]}x + {A[i][1]}y <= {b[i]}')
        else:
            plt.axvline(x=b[i]/A[i][0], color='r', linestyle='--')

    # shade the feasible region
    plt.imshow(region.astype(int), extent=(x.min(), x.max(), y.min(), y.max()), 
               origin="lower", cmap="Greys", alpha=0.3)
    
    # Configure plot settings
    plt.xlim(x_bounds)
    plt.ylim(y_bounds)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.title('Feasible Region')
    plt.show()


if __name__ == "__main__":

    # Initialize problem data
    
    c = [-5, -12]
    
    H_starting = [
        [1,  3, 5],    
        [-7, 3, -1],   
        [1, -1, 3],    
    ]
    
    H_rest = [
        [4, -9, 35],  
        [3, -7, 32],  
        [-2, 5, 26],  
        [-1, 0, 0],   
        [0, -1, 0]    
    ]

    b = [5, -1, 3, 35, 32, 26, 0, 0]
    
    # Execute the incremental algorithm to find the optimal solution
    x_opt, f_opt = incremental_algorithm(c, H_starting, H_rest)

    # Display the final results
    print("FINAL SOLUTION:")
    print("---------------")
    print("Optimal x=", x_opt[0])
    print("Optimal y=", x_opt[1])
    print("F(x)=", f_opt)
    print("---------------")


    plot_feasible_region(H_starting + H_rest, b, x_bounds=(-10, 10), y_bounds=(-10, 10))