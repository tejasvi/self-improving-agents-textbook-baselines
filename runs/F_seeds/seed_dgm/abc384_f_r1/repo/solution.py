import sys
from collections import defaultdict


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]

    # GE[k] = sum of (a_i + a_j) over unordered pairs i<=j with 2^k | (a_i + a_j)
    K = 26  # 2^25 > 2*10^7, so no sum with v >= 25 exists; GE[K] = 0
    GE = [0] * (K + 1)
    for k in range(K):
        M = 1 << k
        mask = M - 1
        cnt = defaultdict(int)
        sm = defaultdict(int)
        for x in a:
            r = x & mask
            cnt[r] += 1
            sm[r] += x
        ordered = 0
        diag = 0
        for r, c in cnt.items():
            p = (-r) & mask
            cp = cnt.get(p, 0)
            if cp:
                ordered += sm[r] * cp
            if (2 * r) & mask == 0:
                diag += 2 * sm[r]
        ordered *= 2  # sum over r of sm[r]*cnt[-r] + cnt[r]*sm[-r]
        GE[k] = (ordered + diag) // 2
    GE[K] = 0

    ans = 0
    for k in range(K):
        E = GE[k] - GE[k + 1]
        ans += E >> k  # E is divisible by 2^k
    print(ans)


main()
