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
    label = [0] * N
    dirs = (1, -1, W2, -W2)
    C = 0
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            p = i * W2 + j
            if green[p] and label[p] == 0:
                C += 1
                label[p] = C
                stack = [p]
                while stack:
                    q = stack.pop()
                    for d in dirs:
                        r = q + d
                        if green[r] and label[r] == 0:
                            label[r] = C
                            stack.append(r)
    R = 0
    total_k = 0
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            p = i * W2 + j
            if not green[p]:
                R += 1
                s = set()
                for d in dirs:
                    l = label[p + d]
                    if l:
                        s.add(l)
                total_k += len(s)
    # sum over red cells of (C + 1 - k) = R*(C+1) - total_k
    num = (R * (C + 1) - total_k) % MOD
    ans = num * pow(R, MOD - 2, MOD) % MOD
    print(ans)

main()
