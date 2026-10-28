import sys


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    MOD = 998244353
    Wp = W + 2
    # padded grid: 1 = green, 0 = red/border
    g = bytearray((H + 2) * Wp)
    for i in range(H):
        row = data[2 + i]
        base = (i + 1) * Wp + 1
        for j in range(W):
            if row[j] == 35:  # '#'
                g[base + j] = 1
    label = [0] * ((H + 2) * Wp)
    C = 0
    for s in range(len(g)):
        if g[s] and not label[s]:
            C += 1
            label[s] = C
            stack = [s]
            while stack:
                v = stack.pop()
                for u in (v - 1, v + 1, v - Wp, v + Wp):
                    if g[u] and not label[u]:
                        label[u] = C
                        stack.append(u)
    total = 0
    red = 0
    for i in range(1, H + 1):
        base = i * Wp
        for v in range(base + 1, base + W + 1):
            if g[v]:
                continue
            red += 1
            a = label[v - 1]
            b = label[v + 1]
            c = label[v - Wp]
            d = label[v + Wp]
            k = 0
            seen = []
            for x in (a, b, c, d):
                if x and x not in seen:
                    seen.append(x)
            k = len(seen)
            total += C + 1 - k
    ans = total % MOD * pow(red % MOD, MOD - 2, MOD) % MOD
    print(ans)


main()
