#!/usr/bin/env python3

class UnionFind:
    def __init__(self):
        self.parent = {}
    
    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px = self.find(x)
        py = self.find(y)
        if px != py:
            self.parent[px] = py

def solve():
    n = int(input())
    products = []
    for _ in range(n):
        products.append(input().strip())
    
    # Build a directed graph where each letter is a node
    # and each product name is an edge
    in_degree = {}
    out_degree = {}
    uf = UnionFind()
    
    # Initialize all letters that appear
    for product in products:
        first_letter = product[0]
        second_letter = product[1]
        
        if first_letter not in out_degree:
            out_degree[first_letter] = 0
            in_degree[first_letter] = 0
        if second_letter not in in_degree:
            in_degree[second_letter] = 0
            out_degree[second_letter] = 0
        
        # Union the two letters to track connected components
        uf.union(first_letter, second_letter)
    
    # Count degrees for each edge
    for product in products:
        first_letter = product[0]
        second_letter = product[1]
        out_degree[first_letter] += 1
        in_degree[second_letter] += 1
    
    # Group vertices by connected component
    components = {}
    for letter in out_degree:
        root = uf.find(letter)
        if root not in components:
            components[root] = []
        components[root].append(letter)
    
    # For each connected component, calculate the minimum number of paths
    total_paths = 0
    for component_letters in components.values():
        # Count vertices with out_degree > in_degree in this component
        excess_out = sum(1 for letter in component_letters 
                        if out_degree[letter] > in_degree[letter])
        
        # If all vertices have equal in and out degree, we need 1 path (Eulerian)
        # Otherwise we need as many paths as vertices with excess out-degree
        if excess_out == 0:
            total_paths += 1
        else:
            total_paths += excess_out
    
    print(total_paths)

solve()
