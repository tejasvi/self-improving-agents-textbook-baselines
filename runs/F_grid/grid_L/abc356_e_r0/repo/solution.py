import sys
from itertools import accumulate


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    m = max(a)
    cnt = [0] * (m + 1)
    for v in a:
        cnt[v] += 1
    # P[v] = number of elements <= v
    P = list(accumulate(cnt))
    total = 0
    for x in range(1, m + 1):
        c = cnt[x]
        if c == 0:
            continue
        q = m // x
        # S = sum_{y in A} floor(y / x) = sum_{k=1}^{q} (n - P[kx-1])
        s = q * n - sum(P[x - 1:m:x])
        # self pairs contribute 1 each (c of them, counted via k=1 term);
        # equal-value pairs are counted twice across ordered visits.
        total += c * (s - 1) - c * (c - 1) // 2
    print(total)


main()
