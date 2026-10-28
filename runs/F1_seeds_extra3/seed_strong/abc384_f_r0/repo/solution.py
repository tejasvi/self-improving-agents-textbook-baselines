import sys
from collections import Counter
from itertools import repeat
from operator import mul


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    mx = max(A)
    # f(s) = odd part of s. Using 2^{-v} = 1 - sum_{k=1}^{v} 2^{-k} (v = v2(s) >= 0):
    # ans = S_0 - sum_{k>=1} S_k / 2^k, where S_k = sum over pairs i<=j with 2^k | A_i+A_j
    # of (A_i+A_j). Scaled by 2^K to stay in integers.
    K = max(1, (2 * mx).bit_length())
    total = ((n + 1) * sum(A)) << K
    for k in range(1, K + 1):
        mask = (1 << k) - 1
        rs = [a & mask for a in A]
        cnt = Counter(rs)
        # ordered pairs (i,j), including i=j: sum of (a_i+a_j) with a_i+a_j = 0 mod 2^k
        # = 2 * sum_i a_i * cnt[-a_i mod 2^k]
        nrs = [(-r) & mask for r in rs]
        ordered = 2 * sum(map(mul, A, map(cnt.get, nrs, repeat(0))))
        # diagonal (i=j) pairs were counted once in ordered (as 2a_i) -> correct count
        # ordered counts each unordered i<j twice and i=j once with weight 2a_i; sum over i<=j:
        # (ordered + diag)/2 where diag = sum over i with 2a_i = 0 mod 2^k of 2a_i
        diag = 0
        if mask:
            for a in A:
                if (2 * a) & mask == 0:
                    diag += 2 * a
        total -= ((ordered + diag) // 2) << (K - k)
    print(total >> K)


main()
