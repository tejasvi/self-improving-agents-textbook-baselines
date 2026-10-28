import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]
    W2 = W + 2
    # padded grid: 1 = green, 0 = red/border
    g = bytearray((H + 2) * W2)
    for i in range(H):
        r = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if r[j] == 35:  # '#'
                g[base + j] = 1
    comp = [0] * ((H + 2) * W2)
    C = 0
    for idx in range(len(g)):
        if g[idx] and not comp[idx]:
            C += 1
            comp[idx] = C
            stack = [idx]
            while stack:
                v = stack.pop()
                for u in (v - 1, v + 1, v - W2, v + W2):
                    if g[u] and not comp[u]:
                        comp[u] = C
                        stack.append(u)
    MOD = 998244353
    total = 0
    R = 0
    for i in range(1, H + 1):
        base = i * W2
        for idx in range(base + 1, base + W + 1):
            if not g[idx]:
                R += 1
                a = comp[idx - 1]; b = comp[idx + 1]
                c = comp[idx - W2]; d = comp[idx + W2]
                k = 0
                s = set((a, b, c, d))
                s.discard(0)
                k = len(s)
                total += C + 1 - k
    ans = total % MOD * pow(R % MOD, MOD - 2, MOD) % MOD
    print(ans)

main()
