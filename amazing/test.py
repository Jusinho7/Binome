# test_gen.py
from mazegen.generator import MazeGenerator

def validate(maze: MazeGenerator) -> bool:
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            if x + 1 < maze.width:
                east_open = not (cell & MazeGenerator.EAST)
                west_open = not (maze.grid[y][x+1] & MazeGenerator.WEST)
                if east_open != west_open:
                    print(f"Incohérence EST/OUEST en ({x},{y})")
                    return False
            if y + 1 < maze.height:
                south_open = not (cell & MazeGenerator.SOUTH)
                north_open = not (maze.grid[y+1][x] & MazeGenerator.NORTH)
                if south_open != north_open:
                    print(f"Incohérence SUD/NORD en ({x},{y})")
                    return False
    return True


maze = MazeGenerator(width=10, height=8, seed=42)
maze.print_ascii()
print("Valide :", validate(maze))