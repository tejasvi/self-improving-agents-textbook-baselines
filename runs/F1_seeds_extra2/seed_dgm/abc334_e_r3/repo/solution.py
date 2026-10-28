import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    H, W = int(data[0]), int(data[1])
    rows = data[2:2 + H]
    W2 = W + 2
    N = (H + 2) * W2
    green = bytearray(N)
    for i in range(H):
        row = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if row[j] == '#':
                green[base + j] = 1
    comp = [-1] * N
    C = 0
    for s in range(N):
        if green[s] and comp[s] < 0:
            comp[s] = C
            dq = deque([s])
            while dq:
                u = dq.popleft()
                for v in (u - 1, u + 1, u - W2, u + W2):
                    if green[v] and comp[v] < 0:
                        comp[v] = C
                        dq.append(v)
            C += 1
    total = 0
    reds = 0
    for i in range(H):
        base = (i + 1) * W2 + 1
        for j in range(W):
            u = base + j
            if not green[u]:
                reds += 1
                labels = set()
                for v in (u - 1, u + 1, u - W2, u + W2):
                    if green[v]:
                        labels.add(comp[v])
                total += C + 1 - len(labels)
    MOD = 998244353
    ans = total % MOD * pow(reds % MOD, MOD - 2, MOD) % MOD
    print(ans)

main()
