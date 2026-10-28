import sys
from collections import Counter
from operator import mul


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    # T_k = sum over pairs i<=j with 2^k | (A_i+A_j) of (A_i+A_j)
    LIM = 27
    T = [0] * (LIM + 2)
    for k in range(LIM + 1):
        M = 1 << k
        mask = M - 1
        r = [a & mask for a in A]
        cnt = Counter(r)
        p = [(-x) & mask for x in r]
        pc = list(map(cnt.__getitem__, p))
        ordered = 2 * sum(map(mul, A, pc))
        diag = 0
        for a in A:
            b = 2 * a
            if b & mask == 0:
                diag += b
        T[k] = (ordered + diag) // 2
    ans = 0
    for k in range(LIM + 1):
        ans += (T[k] - T[k + 1]) >> k
    print(ans)


main()
