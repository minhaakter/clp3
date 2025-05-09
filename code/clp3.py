import random
from collections import deque

class Node:
    def __init__(self, x, y, level, parent=None):
        self.x = x
        self.y = y
        self.level = level
        self.parent = parent  # To track path

class BFS_2D_Traversal:
    def __init__(self):
        self.directions = [(1, 0, "Down"), (-1, 0, "Up"), (0, 1, "Right"), (0, -1, "Left")]
        self.found = False
        self.goal_level = 0
        self.N = 0
        self.source = None
        self.goal = None
        self.path = []
        
    def generate_grid(self, N, obstacle_prob=0.3):
        """Generate NxN grid with random obstacles (0=obstacle, 1=free)"""
        grid = [[1 for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if random.random() < obstacle_prob:
                    grid[i][j] = 0
        return grid
    
    def print_grid(self, grid, show_path=False):
        """Print the grid with S for start, G for goal, 0 for obstacle, 1 for free"""
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if show_path and (i, j) in self.path:
                    print("*", end=" ")
                elif (i, j) == (self.source.x, self.source.y):
                    print("S", end=" ")
                elif (i, j) == (self.goal.x, self.goal.y):
                    print("G", end=" ")
                else:
                    print(grid[i][j], end=" ")
            print()
    
    def get_user_input(self):
        """Get grid size, start and goal positions from user"""
        self.N = int(input("Enter grid size (N): "))
        grid = self.generate_grid(self.N)
        
        # First print the plain grid
        print("\nGenerated grid (0=obstacle, 1=free):")
        for row in grid:
            print(' '.join(map(str, row)))
        
        print("\nEnter starting position (row and column, 0-based):")
        source_x = int(input("Row: "))
        source_y = int(input("Column: "))
        
        print("\nEnter goal position (row and column, 0-based):")
        goal_x = int(input("Row: "))
        goal_y = int(input("Column: "))
        
        # Validate positions
        if (not (0 <= source_x < self.N and 0 <= source_y < self.N) or
            not (0 <= goal_x < self.N and 0 <= goal_y < self.N)):
            print("Invalid positions! Must be within 0 to", self.N-1)
            return None
        
        if grid[source_x][source_y] == 0:
            print("Start position is blocked!")
            return None
        if grid[goal_x][goal_y] == 0:
            print("Goal position is blocked!")
            return None
            
        self.source = Node(source_x, source_y, 0)
        self.goal = Node(goal_x, goal_y, float('inf'))
        
        # Now print grid with S and G markers
        print("\nGrid with start (S) and goal (G):")
        self.print_grid(grid)
        return grid
    
    def st_bfs(self, graph):
        """Perform BFS and print moves during traversal"""
        queue = deque()
        queue.append(self.source)
        graph[self.source.x][self.source.y] = 0  # Mark start as visited
        
        while queue:
            u = queue.popleft()
            
            for dx, dy, move_name in self.directions:
                v_x, v_y = u.x + dx, u.y + dy
                
                # Check boundaries and if cell is free
                if (0 <= v_x < self.N and 0 <= v_y < self.N and 
                    graph[v_x][v_y] == 1):
                    
                    v_level = u.level + 1
                    child = Node(v_x, v_y, v_level, u)
                    
                    # Print the move
                    print(f"Moving {move_name} -> ({v_x}, {v_y})")
                    
                    if v_x == self.goal.x and v_y == self.goal.y:
                        self.found = True
                        self.goal_level = v_level
                        self._reconstruct_path(child)
                        return
                    
                    graph[v_x][v_y] = 0  # Mark as visited
                    queue.append(child)
    
    def _reconstruct_path(self, node):
        """Reconstruct path from goal to start by following parents"""
        self.path = []
        while node:
            self.path.append((node.x, node.y))
            node = node.parent
        self.path.reverse()  # Reverse to get start->goal order
    
    def print_path(self):
        """Print the path from start to goal"""
        if not self.found:
            print("No path found!")
            return
            
        print("\nPath from start to goal:")
        for i, (x, y) in enumerate(self.path):
            if i == 0:
                print(f"Start -> ({x}, {y})")
            elif i == len(self.path) - 1:
                print(f"Goal -> ({x}, {y})")
            else:
                print(f"Step {i} -> ({x}, {y})")
        
        # Print grid with path
        print("\nGrid with path (marked with *):")
        # Create a fresh grid for visualization
        grid = self.generate_grid(self.N)
        self.print_grid(grid, show_path=True)
    
    def run(self):
        """Main method to run the program"""
        print("=== 2D BFS Traversal ===")
        print("Generating random grid with obstacles...\n")
        
        graph = self.get_user_input()
        if not graph:
            print("\nExiting due to invalid input...")
            return
            
        print("\nStarting BFS traversal...")
        self.st_bfs(graph)
        
        if self.found:
            print("\nGoal found!")
            print("Number of moves required =", self.goal_level)
            self.print_path()
        else:
            print("\nGoal cannot be reached from starting block")

# Run the program
if __name__ == "__main__":
    bfs = BFS_2D_Traversal()
    bfs.run()