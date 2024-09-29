import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

class LinearProgramming:
    
    def __init__(self, c, H_starting, H_rest):
        self.c = c
        self.H_starting = H_starting
        self.H_rest = H_rest
    
    # Find the optimal solution for given constraints
    def partial_solution(self, A, b):
        
        solution = linprog(self.c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method='highs') 

        if solution.success:
            return solution.x, -solution.fun 
        
        return None, None


    # Returns optimal x, f 
    def new_solution(self, constraints, H_new, x_opt):
        
        # Check if x_opt satisfies the new constraint (H_new)
        if np.dot(H_new[:2], x_opt) <= H_new[2]:
            return x_opt, -np.dot(self.c, x_opt)
        
        # If not solve a new problem
        A = np.array([c[:2] for c in constraints])
        b = np.array([c[2] for c in constraints])
        
        # Add new constraint
        updated_constraints = []
        for i in range(len(A)):
            new_constarints = [
                A[i][0] - H_new[0], 
                A[i][1] - H_new[1], 
                b[i] - H_new[2]
            ]
            updated_constraints.append(new_constarints)

        A_new = np.array([constraint[:2] for constraint in updated_constraints])
        b_new = np.array([constraint[2] for constraint in updated_constraints])
        
        # Solve new problem
        return self.partial_solution(A_new, b_new)

    def incremental_algorithm(self):

        # Initial constraint matrix A and vector b from H_starting
        A = [constraint[:2] for constraint in self.H_starting]  
        b = [constraint[2] for constraint in self.H_starting]   

        # Find the optimal solution for the initial set of constraints
        x_opt, f_opt = self.partial_solution(A, b)
        
        # If no solution terminate
        if x_opt is None:
            return
        
        # Add each constraint in the set
        for _, H_new in enumerate(self.H_rest, start=1):

            # Solve new subproblem
            x_opt, f_opt = self.new_solution(self.H_starting, H_new, x_opt)
            
            # If no solution terminate
            if x_opt is None:
                return
            
            # Add new constraint in checked constarint set
            self.H_starting.append(H_new)
        
        return x_opt, f_opt


    # plot the feasible region

    #https://stackoverflow.com/questions/57017444/how-to-visualize-feasible-region-for-linear-programming-with-arbitrary-inequali/57017638#57017638
    def plot_feasible_region(self, A, b, x_bounds, y_bounds):
       
        # generate a grid of x and y values
        x = np.linspace(x_bounds[0], x_bounds[1], 400)
        y = np.linspace(y_bounds[0], y_bounds[1], 400)
        x_grid, y_grid = np.meshgrid(x, y)

        region = np.ones_like(x_grid, dtype=bool)

        for i in range(len(A)):
            # check if A[i][0]*x + A[i][1]*y <= b[i]
            region &= (A[i][0] * x_grid + A[i][1] * y_grid <= b[i])

        # Plot each constraint line
        for i in range(len(A)):
            if A[i][1] != 0:
                y_line = (b[i] - A[i][0] * x) / A[i][1]
                plt.plot(x, y_line, label=f'{A[i][0]}x + {A[i][1]}y <= {b[i]}')
            else:
                plt.axvline(x=b[i]/A[i][0], color='r', linestyle='--')

        # shade the feasible region
        plt.imshow(region.astype(int), extent=(x.min(), x.max(), y.min(), y.max()), 
                   origin="lower", cmap="Greys", alpha=0.3)

        plt.xlim(x_bounds)
        plt.ylim(y_bounds)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)
        plt.title('Feasible Region')
        plt.show()


if __name__ == "__main__":

    # Initialize problem
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
    
    # Inistialise class
    incremental_lp = LinearProgramming(c, H_starting, H_rest)

    x_opt, f_opt = incremental_lp.incremental_algorithm()

    # Display the final results
    print("FINAL SOLUTION:")
    print("---------------")
    print("Optimal x =", x_opt[0])
    print("Optimal y =", x_opt[1])
    print("F(x) =", f_opt)
    print("---------------")

    # Plot the feasible region
    incremental_lp.plot_feasible_region(H_starting , b, x_bounds=(-5, 5), y_bounds=(-5, 5))
