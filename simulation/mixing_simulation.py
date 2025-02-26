import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Grid size
size = 50

def initialize_grid():
    """Initialize a grid with two separate fluids (e.g., coffee and milk)"""
    grid = np.zeros((size, size))
    grid[:, :size//2] = 1  # One half coffee (value 1)
    grid[:, size//2:] = 0  # One half milk (value 0)
    return grid

def update_grid(grid):
    """Simulate diffusion step by averaging neighboring cells."""
    new_grid = grid.copy()
    for i in range(1, size-1):
        for j in range(1, size-1):
            new_grid[i, j] = 0.25 * (grid[i+1, j] + grid[i-1, j] + grid[i, j+1] + grid[i, j-1])
    return new_grid

def compute_entropy(grid):
    """Compute entropy as a measure of disorder in the system."""
    p = grid.flatten()
    p = p[p > 0]  # Avoid log(0)
    return -np.sum(p * np.log(p))

def compute_complexity(grid):
    """Compute complexity as a measure of structure (variance in the system)."""
    return np.var(grid)

# Initialize
grid = initialize_grid()
frames = 100  # Number of animation steps
entropy_values = []
complexity_values = []

def update(frame):
    global grid
    grid = update_grid(grid)
    entropy_values.append(compute_entropy(grid))
    complexity_values.append(compute_complexity(grid))
    ax1.clear()
    ax1.imshow(grid, cmap='hot', interpolation='nearest')
    ax1.set_title("Fluid Mixing Simulation")
    ax2.clear()
    ax2.plot(entropy_values, label='Entropy')
    ax2.plot(complexity_values, label='Complexity')
    ax2.legend()
    ax2.set_title("Entropy & Complexity Over Time")
    ax2.set_xlabel("Time")

def run_simulation():
    global fig, ax1, ax2
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=100)
    plt.show()

run_simulation()
