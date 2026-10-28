# Write your solution here. Read from stdin, write to stdout.

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

def main():
    N, Q = map(int, input().split())
    
    # Initialize: cell i has color i (0-indexed: cell i has color i+1)
    colors = [i + 1 for i in range(N)]
    
    # Union-Find to track connected components
    uf = UnionFind(N)
    
    for _ in range(Q):
        query = list(map(int, input().split()))
        
        if query[0] == 1:
            # Type 1: repaint
            x = query[1] - 1  # Convert to 0-indexed
            c = query[2]
            
            # Find all cells connected to x with the same color
            original_color = colors[x]
            
            # BFS/DFS to find all connected cells with the same color
            to_process = [x]
            processed = set([x])
            
            while to_process:
                curr = to_process.pop()
                colors[curr] = c
                
                # Check left neighbor
                if curr > 0 and curr - 1 not in processed and colors[curr - 1] == original_color:
                    processed.add(curr - 1)
                    to_process.append(curr - 1)
                
                # Check right neighbor
                if curr < N - 1 and curr + 1 not in processed and colors[curr + 1] == original_color:
                    processed.add(curr + 1)
                    to_process.append(curr + 1)
            
            # Union all connected cells
            for cell in processed:
                if cell > 0 and colors[cell] == colors[cell - 1]:
                    uf.union(cell, cell - 1)
                if cell < N - 1 and colors[cell] == colors[cell + 1]:
                    uf.union(cell, cell + 1)
        
        else:
            # Type 2: count cells with color c
            c = query[1]
            count = sum(1 for color in colors if color == c)
            print(count)

if __name__ == "__main__":
    main()
