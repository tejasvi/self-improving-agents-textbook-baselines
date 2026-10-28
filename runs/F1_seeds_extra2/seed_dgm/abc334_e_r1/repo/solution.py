import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    H = int(data[0])
    W = int(data[1])
    rows = data[2:2 + H]
    MOD = 998244353

    # Padded grid of width W+2 with red border to avoid bounds checks.
    W2 = W + 2
    N = (H + 2) * W2
    green = bytearray(N)
    for i in range(H):
        row = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if row[j] == '#':
                green[base + j] = 1

    label = [0] * N
    dirs = (1, -1, W2, -W2)
    C = 0
    for v in range(N):
        if green[v] and label[v] == 0:
            C += 1
            label[v] = C
            dq = deque([v])
            while dq:
                u = dq.popleft()
                for d in dirs:
                    w = u + d
                    if green[w] and label[w] == 0:
                        label[w] = C
                        dq.append(w)

    total = 0
    red_count = 0
    for i in range(1, H + 1):
        base = i * W2
        for j in range(1, W + 1):
            v = base + j
            if green[v]:
                continue
            red_count += 1
            seen = set()
            for d in dirs:
                l = label[v + d]
                if l:
                    seen.add(l)
            total += C + 1 - len(seen)

    ans = total % MOD * pow(red_count % MOD, MOD - 2, MOD) % MOD
    print(ans)


main()
