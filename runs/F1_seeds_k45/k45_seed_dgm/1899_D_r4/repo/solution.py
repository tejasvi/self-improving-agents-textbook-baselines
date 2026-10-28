# Write your solution here. Read from stdin, write to stdout.

from collections import defaultdict
from fractions import Fraction

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # We need to find pairs (i, j) where i < j such that:
        # a_i * 2^(a_j) = a_j * 2^(a_i)
        # Which is equivalent to: a_i / 2^(a_i) = a_j / 2^(a_j)
        
        # For small values of a_i, we compute the exact fraction
        # For large values (> 60), they are all distinct and non-equal to others
        # because the function f(x) = x / 2^x is strictly decreasing for x > 1
        
        groups = defaultdict(int)
        
        for val in a:
            if val <= 60:
                # Compute a_i / 2^(a_i) as a fraction
                # Use Fraction to handle the division properly
                power_of_2 = 1 << val
                frac = Fraction(val, power_of_2)
                key = (frac.numerator, frac.denominator)
            else:
                # For large values, each value is unique
                # because f(x) = x / 2^x is strictly decreasing for x >= 1
                key = ('large', val)
            
            groups[key] += 1
        
        # Count pairs
        count = 0
        for freq in groups.values():
            # Number of pairs from a group of size freq is C(freq, 2)
            count += freq * (freq - 1) // 2
        
        print(count)

solve()
