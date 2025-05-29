# tools/maze_runner.py

import random
import os
import time

# Maze generation (reused from maze_generator.py for consistency)
def generate_maze(width, height):
    grid = [['#' for _ in range(width)] for _ in range(height)]

    def is_valid(r, c):
        return 0 <= r < height and 0 <= c < width

    def carve_path(r, c):
        grid[r][c] = ' '
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            wr, wc = r + dr // 2, c + dc // 2

            if is_valid(nr, nc) and grid[nr][nc] == '#':
                grid[wr][wc] = ' '
                carve_path(nr, nc)

    start_r, start_c = 0, 0
    carve_path(start_r, start_c)
    
    # Set start and end points
    grid[start_r][start_c] = 'S'
    end_r, end_c = height - 1, width - 1
    # Ensure end point is accessible if it started as a wall.
    # Simple approach: If it's a wall, make it a path.
    if grid[end_r][end_c] == '#':
        grid[end_r][end_c] = ' '
    grid[end_r][end_c] = 'E'

    return grid, (start_r, start_c), (end_r, end_c)


def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_maze(maze_grid, player_pos):
    """Prints the maze with the player's current position."""
    clear_screen()
    display_grid = [row[:] for row in maze_grid] # Create a copy
    pr, pc = player_pos
    
    # Only place 'P' if it's not the start or end cell
    # The 'S' and 'E' should remain visible if the player is on them
    original_char = display_grid[pr][pc]
    if original_char == ' ':
        display_grid[pr][pc] = 'P'
    elif original_char == 'S': # Keep 'S' visible if player starts on it
        display_grid[pr][pc] = 'S'
    elif original_char == 'E': # Keep 'E' visible if player reaches it
        display_grid[pr][pc] = 'P' # Show player *on* the exit

    for row in display_grid:
        print("".join(row))


def main():
    """
    A text-based maze navigation game.
    """
    print("--- Text-Based Maze Runner ---")
    print("Navigate the maze using W (Up), A (Left), S (Down), D (Right).")
    print("Reach the 'E' to win! 'S' is your starting point.")
    print("Type 'exit' to quit.")
    print("------------------------------")

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

    maze_grid, start_pos, end_pos = generate_maze(width, height)
    player_pos = list(start_pos) # Player's current position [row, col]

    # Adjust start position on grid if it was a wall, to ensure player can start there
    maze_grid[start_pos[0]][start_pos[1]] = 'S' # Ensure start is marked
    maze_grid[end_pos[0]][end_pos[1]] = 'E'     # Ensure end is marked

    print_maze(maze_grid, player_pos)
    print("\nReady to move? (W/A/S/D + Enter)")

    while True:
        move = input("Your move: ").strip().lower()

        if move == 'exit':
            print("Exiting maze runner. Thanks for playing!")
            break

        dr, dc = 0, 0
        if move == 'w': dr = -1
        elif move == 's': dr = 1
        elif move == 'a': dc = -1
        elif move == 'd': dc = 1
        else:
            print("Invalid move. Use W, A, S, D, or 'exit'.")
            continue

        new_r, new_c = player_pos[0] + dr, player_pos[1] + dc

        # Check boundaries
        if not (0 <= new_r < height and 0 <= new_c < width):
            print("Cannot move off the maze!")
            time.sleep(1)
            continue

        # Check for walls
        if maze_grid[new_r][new_c] == '#':
            print("Ouch! You hit a wall!")
            time.sleep(1)
            continue

        player_pos[0], player_pos[1] = new_r, new_c
        print_maze(maze_grid, player_pos)

        if player_pos[0] == end_pos[0] and player_pos[1] == end_pos[1]:
            print("\n!!! Congratulations! You reached the exit (E)! !!!")
            break
    
    print("\n--- Game Over ---")

# Do NOT call main() here. H7T does that automatically.
