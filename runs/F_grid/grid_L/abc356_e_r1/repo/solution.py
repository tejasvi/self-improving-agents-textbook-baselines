import sys
from itertools import accumulate


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    M = max(a)
    cnt = [0] * (M + 1)
    for x in a:
        cnt[x] += 1
    # P[x] = number of elements <= x
    P = list(accumulate(cnt))
    total = 0
    for v in range(1, M + 1):
        c = cnt[v]
        if c == 0:
            continue
        # pairs of equal values contribute 1 each
        total += c * (c - 1) // 2
        K = M // v
        # S = sum over elements x > v of floor(x / v)
        #   = K*n - sum_{k=1..K} P[k*v-1] - c   (k=1 bucket excludes v itself)
        S = K * n - sum(P[v - 1:K * v:v]) - c
        total += c * S
    print(total)


main()
