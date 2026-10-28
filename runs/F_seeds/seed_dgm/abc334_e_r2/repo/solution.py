import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    H, W = int(data[0]), int(data[1])
    rows = data[2:2 + H]
    MOD = 998244353
    W2 = W + 2
    N = (H + 2) * W2
    green = bytearray(N)
    for i in range(H):
        row = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if row[j] == '#':
                green[base + j] = 1
    label = [0] * N  # 0 = unlabeled
    C = 0
    dirs = (1, -1, W2, -W2)
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            p = i * W2 + j
            if green[p] and label[p] == 0:
                C += 1
                label[p] = C
                dq = deque([p])
                while dq:
                    q = dq.popleft()
                    for d in dirs:
                        r = q + d
                        if green[r] and label[r] == 0:
                            label[r] = C
                            dq.append(r)
    total = 0
    red = 0
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            p = i * W2 + j
            if not green[p]:
                red += 1
                s = set()
                for d in dirs:
                    l = label[p + d]
                    if l:
                        s.add(l)
                total += C + 1 - len(s)
    ans = total % MOD * pow(red % MOD, MOD - 2, MOD) % MOD
    print(ans)

main()
