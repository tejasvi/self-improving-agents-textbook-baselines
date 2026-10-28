import sys
from itertools import accumulate


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    holes = [[] for _ in range(H)]
    idx = 3
    for _ in range(N):
        a = int(data[idx]) - 1
        b = int(data[idx + 1]) - 1
        idx += 2
        holes[a].append(b)

    # dp[j] = largest holeless square with bottom-right corner at (i, j).
    # dp_i[j] = 1 + min(dp_{i-1}[j], dp_{i-1}[j-1], dp_i[j-1]) (0 at holes).
    # Writing y_j = dp_i[j] - j turns the in-row dependency into a prefix min:
    # y_j = min(m_j + 1 - j, y_{j-1}), where m_j = min(prev[j], prev[j-1]).
    prev = [0] * W
    total = 0
    rng = range(W)
    for i in range(H):
        P = [0] + prev
        c = [min(P[j + 1], P[j]) + 1 - j for j in rng]
        for b in holes[i]:
            c[b] = -b
        y = list(accumulate(c, min))
        cur = [y[j] + j for j in rng]
        total += sum(cur)
        prev = cur
    print(total)


main()
