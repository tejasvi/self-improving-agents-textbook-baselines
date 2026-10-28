import sys
from collections import defaultdict


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    maxs = 2 * max(a) if a else 0

    def S(k):
        # sum of (a_i + a_j) over pairs i<=j with 2^k | (a_i + a_j)
        M = 1 << k
        if M > maxs:
            return 0
        mask = M - 1
        cnt = defaultdict(int)
        sm = defaultdict(int)
        for x in a:
            r = x & mask
            cnt[r] += 1
            sm[r] += x
        T = 0
        diag = 0
        for r, c in cnt.items():
            q = (M - r) & mask
            cq = cnt.get(q)
            if cq is None:
                continue
            T += sm[r] * cq + c * sm[q]
            if q == r:
                # diagonal elements with 2*a_i ≡ 0 mod M
                diag += 2 * sm[r]
        # Ordered total T includes diagonal once; unordered i<=j:
        return (T + diag) // 2

    total = 0
    prev = S(0)
    k = 0
    while True:
        nxt = S(k + 1)
        total += (prev - nxt) >> k
        if prev == 0 or (1 << k) > maxs:
            break
        prev = nxt
        k += 1
    print(total)


main()
