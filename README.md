This code sets up an automated virus expansion simulation using a Tkinter GUI, where the virus spreads on a map image overlay based on a grid system. Features:

1.Grid Setup and Initialization:
-The grid is created with dimensions defined by GRID_SIZE_X and GRID_SIZE_Y.
-The grid is initially filled with all "Healthy" cells ('H').
-Specific points defined in STARTING_POINTS are set to "Infected" ('I').

2.Map and Grid Overlay:
-A map image is loaded using PIL and an overlay is created where infected cells are tinted red.
-The overlay also includes scale markers at intervals defined by SCALE_INTERVAL.

3.Infection Spread Logic:
-The infection spreads to adjacent healthy cells based on a probability (INFECTION_PROB).
-Each simulation step updates the grid, applying the infection spread logic.

4.Visualization:
-The updated grid is displayed over the map image.
-The Tkinter Canvas widget is used to display the image with the overlay applied.

Automation and Final State:
-The simulation runs in intervals (SPREAD_INTERVAL) using root.after, which continuously updates the grid and map.
-When all regions are infected, a message is displayed on the Tkinter interface.
