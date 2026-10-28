import sys
from collections import defaultdict


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    s = sum(a)

    def g(k):
        # Sum of (A_i + A_j) over pairs i <= j with 2^k dividing A_i + A_j.
        if k == 0:
            # All pairs: ordered sum over i,j is 2*n*s; unordered with i<=j
            # is (2*n*s + diagonal) / 2 where diagonal = sum of 2*A_i = 2*s.
            return (2 * n * s + 2 * s) // 2
        m = (1 << k) - 1
        cnt = defaultdict(int)
        sm = defaultdict(int)
        for x in a:
            r = x & m
            cnt[r] += 1
            sm[r] += x
        total = 0
        for r, c in cnt.items():
            r2 = (-r) & m
            c2 = cnt.get(r2, 0)
            if c2:
                total += sm[r] * c2 + sm[r2] * c
        diag = 0
        for x in a:
            if (2 * x) & m == 0:
                diag += 2 * x
        return (total + diag) // 2

    ans = 0
    k = 0
    gk = g(0)
    while True:
        gk1 = g(k + 1)
        # pairs with valuation exactly k: sum of (A_i+A_j) = gk - gk1,
        # each contributes odd part (sum >> k).
        ans += (gk - gk1) >> k
        if gk1 == 0:
            break
        gk = gk1
        k += 1
    print(ans)


main()
