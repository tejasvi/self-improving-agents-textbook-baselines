# Write your solution here. Read from stdin, write to stdout.
from fractions import Fraction
from collections import Counter

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # For each element, compute a_i / 2^a_i
        values = []
        for ai in a:
            # Use Fraction to handle exact division
            value = Fraction(ai, 2 ** ai)
            values.append(value)
        
        # Count occurrences of each value
        counter = Counter(values)
        
        # Count pairs: for each value appearing c times, add C(c, 2) = c*(c-1)/2
        result = 0
        for count in counter.values():
            result += count * (count - 1) // 2
        
        print(result)

solve()
