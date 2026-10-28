from collections import defaultdict
from fractions import Fraction

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # Group by the value of 2^a / a
        groups = defaultdict(int)
        
        for ai in a:
            # Use Fraction to handle the division precisely
            # We compute 2^ai / ai
            key = Fraction(2**ai, ai)
            groups[key] += 1
        
        # Count pairs
        result = 0
        for count in groups.values():
            result += count * (count - 1) // 2
        
        print(result)

solve()
