#!/usr/bin/env python3

from functools import lru_cache

MOD = 998244353

def solve():
    line = input().split()
    n, m = int(line[0]), int(line[1])
    
    b = list(map(int, input().split()))
    
    def count_components(arr):
        """Count connected components using Union-Find"""
        parent = list(range(n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # Add edges where A[i] <= A[j] for i < j
        for i in range(n):
            for j in range(i + 1, n):
                if arr[i] <= arr[j]:
                    union(i, j)
        
        # Count connected components
        components = len(set(find(i) for i in range(n)))
        return components
    
    # Find indices of -1s
    missing_indices = [i for i in range(n) if b[i] == -1]
    q = len(missing_indices)
    
    if q == 0:
        # No -1s, just compute f(B)
        print(count_components(b) % MOD)
        return
    
    # Use recursion with memoization
    memo = {}
    
    def dp(idx, seq_tuple):
        """
        idx: which -1 position we're filling (index into missing_indices)
        seq_tuple: current state of sequence as tuple
        Returns: sum of components for all ways to complete from this point
        """
        if idx == q:
            seq = list(seq_tuple)
            return count_components(seq)
        
        if seq_tuple in memo:
            return memo[seq_tuple]
        
        pos = missing_indices[idx]
        total = 0
        for val in range(1, m + 1):
            new_seq = list(seq_tuple)
            new_seq[pos] = val
            new_seq_tuple = tuple(new_seq)
            total = (total + dp(idx + 1, new_seq_tuple)) % MOD
        
        memo[seq_tuple] = total
        return total
    
    result = dp(0, tuple(b))
    print(result)

if __name__ == "__main__":
    solve()
