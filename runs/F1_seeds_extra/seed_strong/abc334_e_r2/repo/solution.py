import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]
    MOD = 998244353
    W2 = W + 2
    # padded grid: 0 = red / border, 1 = green
    g = bytearray((H + 2) * W2)
    for i in range(H):
        r = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if r[j] == 35:  # '#'
                g[base + j] = 1
    lab = [0] * ((H + 2) * W2)
    C = 0
    dirs = (1, -1, W2, -W2)
    for idx in range(len(g)):
        if g[idx] and not lab[idx]:
            C += 1
            lab[idx] = C
            stack = [idx]
            while stack:
                u = stack.pop()
                for d in dirs:
                    v = u + d
                    if g[v] and not lab[v]:
                        lab[v] = C
                        stack.append(v)
    total = 0
    R = 0
    for i in range(1, H + 1):
        base = i * W2
        for idx in range(base + 1, base + W + 1):
            if not g[idx]:
                R += 1
                s = set()
                a = lab[idx + 1]
                if a: s.add(a)
                a = lab[idx - 1]
                if a: s.add(a)
                a = lab[idx + W2]
                if a: s.add(a)
                a = lab[idx - W2]
                if a: s.add(a)
                total += C + 1 - len(s)
    ans = total % MOD * pow(R, MOD - 2, MOD) % MOD
    print(ans)

main()
