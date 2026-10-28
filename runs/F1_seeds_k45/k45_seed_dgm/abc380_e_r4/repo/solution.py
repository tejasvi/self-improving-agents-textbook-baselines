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
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        
        return True

def solve():
    n, q = map(int, input().split())
    
    # color[i] = color of cell i (0-indexed)
    color = list(range(1, n + 1))
    
    # Union-Find to track connected components with same color
    uf = UnionFind(n)
    
    # color_count[c] = number of cells with color c
    from collections import defaultdict
    color_count = defaultdict(int)
    for i in range(n):
        color_count[color[i]] += 1
    
    def merge_adjacent_same_color():
        """Merge adjacent cells with the same color"""
        for i in range(n - 1):
            if color[i] == color[i + 1]:
                uf.union(i, i + 1)
    
    def get_component(x):
        """Get all cells in the component containing cell x"""
        root = uf.find(x)
        component = []
        for i in range(n):
            if uf.find(i) == root:
                component.append(i)
        return component
    
    # Initial merge
    merge_adjacent_same_color()
    
    for _ in range(q):
        query = list(map(int, input().split()))
        
        if query[0] == 1:
            # Query type 1: repaint
            x = query[1] - 1  # Convert to 0-indexed
            c = query[2]
            
            # Get the component containing cell x
            component = get_component(x)
            
            # Update color count
            for cell in component:
                color_count[color[cell]] -= 1
                color[cell] = c
                color_count[c] += 1
            
            # Re-merge adjacent cells with same color
            # Rebuild union-find
            uf = UnionFind(n)
            merge_adjacent_same_color()
        
        else:
            # Query type 2: count
            c = query[1]
            print(color_count[c])

solve()
