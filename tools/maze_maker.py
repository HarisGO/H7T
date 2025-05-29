# tools/maze_generator.py

import random

def main():
    """
    Generates and displays a text-based (ASCII) maze.
    """
    print("--- Text-Based Maze Generator ---")

    while True:
        try:
            width = int(input("Enter maze width (odd number, min 5): "))
            height = int(input("Enter maze height (odd number, min 5): "))
            if width < 5 or height < 5 or width % 2 == 0 or height % 2 == 0:
                print("Width and height must be odd numbers and at least 5.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter whole numbers.")

    print("\nGenerating maze...")

    # Initialize grid: all walls, then carve paths
    grid = [['#' for _ in range(width)] for _ in range(height)]

    def is_valid(r, c):
        return 0 <= r < height and 0 <= c < width

    def carve_path(r, c):
        grid[r][c] = ' ' # Carve current cell

        # Define directions (dr, dc)
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)] # Right, Down, Left, Up
        random.shuffle(directions) # Randomize order

        for dr, dc in directions:
            nr, nc = r + dr, c + dc # New cell coordinates
            wr, wc = r + dr // 2, c + dc // 2 # Wall cell coordinates

            if is_valid(nr, nc) and grid[nr][nc] == '#':
                grid[wr][wc] = ' ' # Carve wall between current and new cell
                carve_path(nr, nc) # Recurse

    # Start carving from a random odd cell (0,0 is fine as a start)
    carve_path(0, 0) # Start from top-left corner, it will always be a path.

    # Set entrance and exit (optional, but good for a maze)
    # Ensure entrance and exit are on border and are paths
    grid[0][0] = 'S' # Start
    grid[height - 1][width - 1] = 'E' # End

    # Print the maze
    for row in grid:
        print("".join(row))

    print("\n--- Maze Generation Complete ---")
    print("S = Start, E = End")

# Do NOT call main() here. H7T does that automatically.
