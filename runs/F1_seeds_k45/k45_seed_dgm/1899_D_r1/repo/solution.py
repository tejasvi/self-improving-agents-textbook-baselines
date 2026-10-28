from fractions import Fraction
from collections import Counter

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # Create a mapping of each index to its ratio a_i / 2^{a_i}
        # We use Fraction for exact arithmetic
        ratios = []
        for i in range(n):
            ratio = Fraction(a[i], 2 ** a[i])
            ratios.append(ratio)
        
        # Count pairs with the same ratio
        ratio_count = Counter(ratios)
        
        # For each ratio that appears k times, we can choose 2 items from k
        # which gives us k*(k-1)/2 pairs
        result = 0
        for count in ratio_count.values():
            result += count * (count - 1) // 2
        
        print(result)

solve()
