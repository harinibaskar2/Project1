import sys
from collections import deque
import heapq


def parse_world(file_path):
    with open(file_path, 'r') as f:
        cols = int(f.readline())
        rows = int(f.readline())
        grid = [list(f.readline().strip()) for _ in range(rows)]

    start = None
    dirty = set()

    for y in range(rows):
        for x in range(cols):
            cell = grid[y][x]
            if cell == '@':
                start = (x, y)
            elif cell == '*':
                dirty.add((x, y))

    return grid, start, dirty

MOVES = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}

def get_neighbors(state, grid):
    x, y = state[0]
    dirty = state[1]
    rows, cols = len(grid), len(grid[0])
    neighbors = []

    # Try moving in all directions
    for action, (dx, dy) in MOVES.items():
        nx, ny = x + dx, y + dy
        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] != '#':
            neighbors.append(((nx, ny), dirty.copy(), action))

    # Try vacuuming if on dirty cell
    if (x, y) in dirty:
        new_dirty = dirty.copy()
        new_dirty.remove((x, y))
        neighbors.append(((x, y), new_dirty, 'V'))

    return neighbors

def dfs(grid, start, dirty):
    stack = [((start, dirty), [])]
    visited = set()
    nodes_generated = 0
    nodes_expanded = 0

    while stack:
        (state, path) = stack.pop()
        robot_pos, dirt = state
        state_key = (robot_pos, frozenset(dirt))

        if state_key in visited:
            continue
        visited.add(state_key)
        nodes_expanded += 1

        if not dirt:
            for action in path:
                print(action)
            print(f"{nodes_generated} nodes generated")
            print(f"{nodes_expanded} nodes expanded")
            return

        for neighbor in get_neighbors(state, grid):
            next_state = (neighbor[0], neighbor[1])
            action = neighbor[2]
            stack.append((next_state, path + [action]))
            nodes_generated += 1

def ucs(grid, start, dirty):
    pq = []
    heapq.heappush(pq, (0, (start, dirty), []))
    visited = set()
    nodes_generated = 0
    nodes_expanded = 0

    while pq:
        cost, state, path = heapq.heappop(pq)
        robot_pos, dirt = state
        state_key = (robot_pos, frozenset(dirt))

        if state_key in visited:
            continue
        visited.add(state_key)
        nodes_expanded += 1

        if not dirt:
            for action in path:
                print(action)
            print(f"{nodes_generated} nodes generated")
            print(f"{nodes_expanded} nodes expanded")
            return

        for neighbor in get_neighbors(state, grid):
            next_state = (neighbor[0], neighbor[1])
            action = neighbor[2]
            heapq.heappush(pq, (cost + 1, next_state, path + [action]))
            nodes_generated += 1
def main():
    print("Starting planner...") 
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py [uniform-cost|depth-first] [world-file]")
        return

    algorithm = sys.argv[1]
    world_file = sys.argv[2]

    grid, start, dirty = parse_world(world_file)

    print("Start:", start)      
    print("Dirty:", dirty)        

    if algorithm == "uniform-cost":
        ucs(grid, start, dirty)
    elif algorithm == "depth-first":
        dfs(grid, start, dirty)
    else:
        print("Invalid algorithm. Use 'uniform-cost' or 'depth-first'.")


if __name__ == "__main__":
    main()