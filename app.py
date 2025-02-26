from flask import Flask, render_template
from flask_socketio import SocketIO
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Grid size
size = 50

def initialize_grid():
    """Initialize a grid with two separate fluids (coffee at the bottom, milk at the top)."""
    grid = np.zeros((size, size))
    grid[:size//2, :] = 1  # Milk on the top (value 1)
    grid[size//2:, :] = 0  # Coffee at the bottom (value 0)
    return grid


# def update_grid(grid):
#     """Simulate diffusion step by averaging neighboring cells."""
#     new_grid = grid.copy()
#     for i in range(1, size-1):
#         for j in range(1, size-1):
#             new_grid[i, j] = 0.25 * (grid[i+1, j] + grid[i-1, j] + grid[i, j+1] + grid[i, j-1])
#     return new_grid

def update_grid(grid, diffusion_rate=0.5):
    """Simulate faster diffusion by considering more neighbors and increasing mixing rate."""
    new_grid = grid.copy()
    for i in range(1, size-1):
        for j in range(1, size-1):
            new_grid[i, j] = (1 - diffusion_rate) * grid[i, j] + diffusion_rate * (
                0.125 * (grid[i+1, j] + grid[i-1, j] + grid[i, j+1] + grid[i, j-1] + 
                         grid[i+1, j+1] + grid[i-1, j-1] + grid[i+1, j-1] + grid[i-1, j+1])
            )
    return new_grid



@app.route("/")
def home():
    return render_template("index.html")

@socketio.on("start_simulation")
def start_simulation():
    """Runs the simulation and sends real-time updates to the frontend"""
    global grid
    grid = initialize_grid()
    entropy_values = []
    complexity_values = []

    for frame in range(10000):
        grid = update_grid(grid)
        entropy_values.append(np.var(grid))  # Simulating entropy
        complexity_values.append(np.var(grid))  # Simulating complexity

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        # Plot fluid mixing
        ax1.imshow(grid, cmap="hot", interpolation="nearest")
        ax1.set_title("Fluid Mixing Simulation")

        # Plot entropy & complexity
        ax2.plot(entropy_values, label="Entropy", color="blue")
        ax2.plot(complexity_values, label="Complexity", color="orange")
        ax2.legend()
        ax2.set_title("Entropy & Complexity Over Time")
        ax2.set_xlabel("Time")

        # Convert plot to PNG
        img_io = io.BytesIO()
        plt.savefig(img_io, format="png")
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode("utf-8")

        plt.close(fig)  # ✅ Close the figure to prevent memory leaks

        # Send update to frontend
        socketio.emit("simulation_update", {"image": img_base64})

        time.sleep(0.01)  # Simulate real-time updates

if __name__ == "__main__":
    socketio.run(app, debug=True)
