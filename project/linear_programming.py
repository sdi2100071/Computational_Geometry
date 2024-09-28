import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog


class LineaProgramming:
    def __init__(self, c):
        self.c = c  # Objective function coefficients

    def partial_solution(self, A, b):
        # Solve the linear program
        solution = linprog(self.c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method='highs')
        
        if solution.success:
            return solution.x, -solution.fun  # Return optimal solution and objective function value
        return None, None

    def new_solution(self, constraints, H_new, x_opt):
        # Check if current optimal solution satisfies the new constraint
        if np.dot(H_new[:2], x_opt) <= H_new[2]:
            return x_opt, -np.dot(self.c, x_opt)  # If valid, return the current solution
        
        # If not, create the new subproblem
        A = np.array([constraint[:2] for constraint in constraints])
        b = np.array([constraint[2] for constraint in constraints])
        
        # Adjust constraints by incorporating the new one
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
        
        # Solve the updated problem
        return self.partial_solution(A_new, b_new)

    def incremental_algorithm(self, H_starting, H_rest):
        # Extract initial constraint matrix and vector
        A = [constraint[:2] for constraint in H_starting]
        b = [constraint[2] for constraint in H_starting]

        # Solve for the partial solution with initial constraints
        x_opt, f_opt = self.partial_solution(A, b)
        
        if x_opt is None:
            return None, None
        
        # Iteratively add new constraints and update the solution
        for H_new in H_rest:
            x_opt, f_opt = self.new_solution(H_starting, H_new, x_opt)
            
            if x_opt is None:
                return None, None  # Stop if no feasible solution
            
            # Add new constraint to the current active set
            H_starting.append(H_new)
        
        return x_opt, f_opt

    def plot_feasible_region(self, A, b, x_bounds, y_bounds):
        # Create grid of x values for plotting
        x_vals = np.linspace(x_bounds[0], x_bounds[1], 400)
        
        # Plot each constraint as a line
        for i in range(len(A)):
            if A[i][1] != 0:
                y_vals = (b[i] - A[i][0] * x_vals) / A[i][1]
                plt.plot(x_vals, y_vals, label=f'{A[i][0]}x + {A[i][1]}y <= {b[i]}')
            else:
                # Handle vertical lines when A[i][1] == 0
                plt.axvline(x=b[i] / A[i][0], color='r', linestyle='--')

        # Shade the feasible region
        y_grid, x_grid = np.meshgrid(np.linspace(y_bounds[0], y_bounds[1], 400), x_vals)
        z = np.ones_like(x_grid)
        
        for i in range(len(A)):
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

    # initilise problem with given data
    
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

    b = np.array([5, -1, 3, 35, 32, 26, 0, 0])

    linprog = LinearProgramming(c)
    
    x_opt, f_opt = linprog.incremental_algorithm(c, H_starting, H_rest)

    print("FINAL SOLUTION:")
    print("---------------")
    print("Optimal x=", x_opt[0])
    print("Optimal y=", x_opt[1])
    print("F(x)=", f_opt)
    print("---------------")

    plot_feasible_region(H_starting + H_rest, b, x_bounds=(-10, 50), y_bounds=(-10, 50))


    
    
    

        