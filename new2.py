import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog


def partial_solution(c, A, b):
    
    # Find the optimal solution for the given constraints
    solution = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method='highs')
    
    if solution.success:
        return solution.x, -solution.fun
    return None, None


# Returns x_opt, f_opt.
def new_solution(constraints, H_new, x_opt):

    # Check if x_opt satisfies the new constraint (H_new)
    if np.dot(H_new[:2], x_opt) <= H_new[2]:
        return x_opt, -np.dot(c, x_opt)
    
    # if x_opt does not satisfy the new constaint

    # Calculate new subproblem
    A = np.array([c[:2] for c in constraints])
    b = np.array([c[2] for c in constraints])
    
    # Create new constraints set by adding the new one
    new_constraints = []
    for i in range(len(A)):
        constraint_set = [
            A[i][0] - H_new[0], 
            A[i][1] - H_new[1], 
            b[i] - H_new[2]
        ]
        new_constraints.append(constraint_set)

    A_new = np.array([constraint[:2] for constraint in new_constraints])
    b_new = np.array([constraint[2] for constraint in new_constraints])
    
    # Solve the new problem
    return partial_solution(c, A_new, b_new)


def incremental_algorithm(c, H_starting, H_rest):
   
    # CHANGEEEEEEEE<<<<<<<<<<<<<<<<<<<<<<<<<<<,    
    A = [constraint[:2] for constraint in H_starting]  
    b = [constraint[2] for constraint in H_starting]   

    # Find partial(optimal) solution for initial set of constraints (H_starting)
    x_opt, f_opt = partial_solution(c, A, b)
    
    if x_opt is None:
        return
    
    for _, H_new in enumerate(H_rest, start=1):
            x_opt, f_opt = new_solution(H_starting, H_new, x_opt)
            
            if x_opt is None:
                return
            
            # Update constraints with the new one.
            H_starting.append(H_new)
        
    return x_opt, f_opt


############### <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def plot_feasible_region(A, b, x_bounds, y_bounds):
    # Create a grid of x values
    x = np.linspace(x_bounds[0], x_bounds[1], 400)
    
    # Plot each constraint line
    for i in range(8):
        if A[i][1] != 0:
            # Rearrange the inequality into y = (b - A[0]*x) / A[1]
            y = (b[i] - A[i][0] * x) / A[i][1]
            plt.plot(x, y, label=f'{A[i][0]}x + {A[i][1]}y <= {b[i]}')
        else:
            # If A[i][1] == 0, plot vertical line
            plt.axvline(x=b[i]/A[i][0], color='r', linestyle='--')

    # Shade the feasible region
    y_grid, x_grid = np.meshgrid(np.linspace(y_bounds[0], y_bounds[1], 400), x)
    z = np.ones_like(x_grid)

    for i in range(8):
        z *= (A[i][0] * x_grid + A[i][1] * y_grid <= b[i])

    plt.contourf(x_grid, y_grid, z, levels=[0, 1], colors=['#e0f7fa'], alpha=0.5)
    
    # Plot settings
    plt.xlim(x_bounds)
    plt.ylim(y_bounds)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.title('Feasible Region')
    plt.show()

    
if __name__ == "__main__":

    # Initilise problem with given data
    
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
    
    x_opt, f_opt = incremental_algorithm(c, H_starting, H_rest)

    print("FINAL SOLUTION:")
    print("---------------")
    print("Optimal x=", x_opt[0])
    print("Optimal y=", x_opt[1])
    print("F(x)=", f_opt)
    print("---------------")

    plot_feasible_region(H_starting + H_rest, b, x_bounds=(-10, 10), y_bounds=(-10, 10))


    
    
    

        
