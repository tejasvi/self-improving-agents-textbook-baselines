import sys

def main():
    data = sys.stdin.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]
    MOD = 998244353
    W2 = W + 2
    # padded grid: green = 1
    g = bytearray((H + 2) * W2)
    for i in range(H):
        row = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if row[j] == '#':
                g[base + j] = 1
    comp = [0] * ((H + 2) * W2)
    C = 0
    dirs = (1, -1, W2, -W2)
    for idx in range(len(g)):
        if g[idx] and not comp[idx]:
            C += 1
            comp[idx] = C
            stack = [idx]
            while stack:
                v = stack.pop()
                for d in dirs:
                    u = v + d
                    if g[u] and not comp[u]:
                        comp[u] = C
                        stack.append(u)
    total = 0
    red = 0
    for i in range(1, H + 1):
        base = i * W2
        for j in range(1, W + 1):
            p = base + j
            if g[p]:
                continue
            red += 1
            labels = set()
            for d in dirs:
                c = comp[p + d]
                if c:
                    labels.add(c)
            total += C + 1 - len(labels)
    ans = total % MOD * pow(red, MOD - 2, MOD) % MOD
    print(ans)

main()
