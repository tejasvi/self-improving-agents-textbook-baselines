from collections import Counter
from fractions import Fraction
import sys

def solve(n, a):
    # Create signatures for comparison
    signatures = []
    for ai in a:
        if ai <= 60:
            sig = ('small', Fraction(ai, 2**ai))
        else:
            sig = ('large', ai)
        signatures.append(sig)
    
    # Count pairs with the same signature
    counter = Counter(signatures)
    
    # For each signature that appears k times, we have C(k, 2) = k*(k-1)/2 pairs
    result = 0
    for count in counter.values():
        result += count * (count - 1) // 2
    
    return result

# Read all input
lines = []
for line in sys.stdin:
    line = line.strip()
    if line:  # Skip blank lines
        lines.append(line)

# Process input
idx = 0
t = int(lines[idx])
idx += 1

for _ in range(t):
    n = int(lines[idx])
    idx += 1
    a = list(map(int, lines[idx].split()))
    idx += 1
    
    result = solve(n, a)
    print(result)
