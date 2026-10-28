from fractions import Fraction
from collections import Counter

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # Compute the key for each element: a_i / 2^{a_i}
        # We use Fraction to handle exact rational arithmetic
        keys = []
        for ai in a:
            # Create fraction a_i / 2^{a_i}
            key = Fraction(ai, 2 ** ai)
            keys.append(key)
        
        # Count occurrences of each key
        counter = Counter(keys)
        
        # Count pairs
        result = 0
        for count in counter.values():
            # If count elements have the same key, they form C(count, 2) pairs
            result += count * (count - 1) // 2
        
        print(result)

solve()
