import sys
from math import isqrt


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1][:n]
    # Squares with at most n digits are k*k < 10^n, i.e. k <= isqrt(10^n - 1).
    m = isqrt(10 ** n - 1) + 1
    # Multiset of digits of S (zeros included), as a sorted string.
    target = ''.join(sorted(s))
    # A square must have the same digit sum as S, hence the same value mod 9.
    total_mod9 = sum(int(c) for c in s) % 9
    # Only k with k*k % 9 == total_mod9 can match; precompute those residues of k.
    good = [r for r in range(9) if (r * r) % 9 == total_mod9]
    ans = 0
    for base in range(0, m, 9):
        for r in good:
            kk = base + r
            if kk >= m:
                continue
            t = str(kk * kk)
            # Pad with leading zeros to n digits; they count as '0' in the multiset.
            if len(t) < n:
                t = '0' * (n - len(t)) + t
            if ''.join(sorted(t)) == target:
                ans += 1
    print(ans)


main()
