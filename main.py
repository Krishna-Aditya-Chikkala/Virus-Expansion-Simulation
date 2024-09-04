import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import random
import numpy as np

# Parameters
GRID_SIZE_X = 320        # Increased number of columns for smaller cells
GRID_SIZE_Y = 204        # Increased number of rows for smaller cells
INFECTION_PROB = 0.5     # Probability of infection spreading
STARTING_POINTS = [(70, 20), (50, 105), (110, 80), (150, 115), (135, 170), (80, 165), (115, 215), (115, 250), (40, 270), (180, 300)]  # List of initial infection points (row, col)
MAP_IMAGE_PATH = 'map.png'  # Path to the map image
SPREAD_INTERVAL = 10     # Interval in milliseconds (1000 ms = 1 second)
TINT_SIZE = None         # Size of the small red tint squares (to be calculated)
SCALE_INTERVAL = 20      # Interval for scale markers (show every 20 cells)
TEXT_OPACITY = 255       # Full opacity for scale numbers

# Create the grid with all individuals healthy
def create_grid(size_x, size_y):
    return np.full((size_y, size_x), 'H')

# Infect specific starting points
def initialize_infected(grid, starting_points):
    for (row, col) in starting_points:
        if 0 <= row < GRID_SIZE_Y and 0 <= col < GRID_SIZE_X:
            grid[row][col] = 'I'

# Overlay the grid on the map image with a red tint
def overlay_grid_on_map(map_img, grid):
    global TINT_SIZE
    # Create a red tint image the same size as the map
    tint = Image.new('RGBA', map_img.size, (255, 0, 0, 0))
    draw = ImageDraw.Draw(tint)
    
    cell_width = map_img.width / GRID_SIZE_X
    cell_height = map_img.height / GRID_SIZE_Y

    if TINT_SIZE is None:
        TINT_SIZE = int(min(cell_width, cell_height))  # Set tint size to exactly fit cell dimensions

    for i in range(GRID_SIZE_Y):
        for j in range(GRID_SIZE_X):
            if grid[i][j] == 'I':
                # Calculate the position for smaller red tint squares
                x0 = j * cell_width
                y0 = i * cell_height
                x1 = x0 + TINT_SIZE
                y1 = y0 + TINT_SIZE
                # Ensure the square completely fills the cell by aligning edges
                x1 = min(x1, map_img.width)  # Prevent drawing outside the map bounds
                y1 = min(y1, map_img.height)  # Prevent drawing outside the map bounds
                # Draw a semi-transparent red rectangle
                draw.rectangle([x0, y0, x1, y1], fill=(255, 0, 0, 128))  # Semi-transparent red

    # Create a scale overlay
    scale = Image.new('RGBA', map_img.size, (0, 0, 0, 0))
    scale_draw = ImageDraw.Draw(scale)
    
    # Draw dotted vertical scales
    for i in range(0, GRID_SIZE_X + 1, SCALE_INTERVAL):
        x = i * cell_width
        for j in range(0, int(map_img.height), 4):  # 4-pixel gaps for dotted effect
            scale_draw.line([(x, j), (x, j + 2)], fill=(0, 0, 0, 128), width=1)
        # Draw scale numbers at intervals with higher opacity
        scale_draw.text((x + 2, 2), str(i), fill=(0, 0, 0, TEXT_OPACITY))

    # Draw dotted horizontal scales
    for i in range(0, GRID_SIZE_Y + 1, SCALE_INTERVAL):
        y = i * cell_height
        for j in range(0, int(map_img.width), 4):  # 4-pixel gaps for dotted effect
            scale_draw.line([(j, y), (j + 2, y)], fill=(0, 0, 0, 128), width=1)
        # Draw scale numbers at intervals with higher opacity
        scale_draw.text((2, y + 2), str(i), fill=(0, 0, 0, TEXT_OPACITY))

    # Combine the map, scale, and the red tint
    combined = Image.alpha_composite(map_img, scale)
    combined = Image.alpha_composite(combined, tint)
    return combined

# Update the grid for the next step of the simulation
def update_grid(grid):
    new_grid = grid.copy()
    for i in range(GRID_SIZE_Y):
        for j in range(GRID_SIZE_X):
            if grid[i][j] == 'I':
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < GRID_SIZE_Y and 0 <= nj < GRID_SIZE_X and grid[ni][nj] == 'H':
                        if random.random() < INFECTION_PROB:
                            new_grid[ni][nj] = 'I'
    return new_grid

# Check if all regions are infected
def all_infected(grid):
    return np.all(grid == 'I')

# Run the simulation automatically every interval
def auto_step_simulation():
    global grid, map_img, map_tk_img, message_displayed
    grid = update_grid(grid)
    updated_map = overlay_grid_on_map(map_img.copy(), grid)
    map_tk_img = ImageTk.PhotoImage(updated_map)
    canvas.create_image(0, 0, anchor=tk.NW, image=map_tk_img)
    
    if all_infected(grid) and not message_displayed:
        message_label.config(text="All regions infected")
        message_displayed = True
    
    root.after(SPREAD_INTERVAL, auto_step_simulation)  # Schedule the next step

# Main UI setup
root = tk.Tk()
root.title("Automated Virus Expansion Simulator with Map Overlay")

# Load the map image
try:
    map_img = Image.open(MAP_IMAGE_PATH).convert("RGBA")
except FileNotFoundError:
    print(f"Error: The file {MAP_IMAGE_PATH} was not found.")
    root.destroy()

canvas = tk.Canvas(root, width=map_img.width, height=map_img.height)
canvas.pack()

# Initialize grid and start simulation
grid = create_grid(GRID_SIZE_X, GRID_SIZE_Y)
initialize_infected(grid, STARTING_POINTS)

# Add a label to display the message
message_displayed = False
message_label = tk.Label(root, text="", font=("Arial", 24), fg="red")
message_label.pack()

# Start the automated simulation
root.after(SPREAD_INTERVAL, auto_step_simulation)

root.mainloop()
