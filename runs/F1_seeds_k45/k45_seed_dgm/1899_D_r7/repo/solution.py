# Write your solution here. Read from stdin, write to stdout.

from collections import defaultdict
from fractions import Fraction

def get_key(a):
    """Get the key value for comparison: a / 2^a"""
    # We use Fraction to get exact rational representation
    return Fraction(a, 2 ** a)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # Count pairs where a_i / 2^a_i == a_j / 2^a_j
        key_count = defaultdict(int)
        
        for val in a:
            key = get_key(val)
            key_count[key] += 1
        
        # For each key, count pairs from elements with that key
        result = 0
        for count in key_count.values():
            # Number of pairs from 'count' elements is C(count, 2)
            result += count * (count - 1) // 2
        
        print(result)

solve()
