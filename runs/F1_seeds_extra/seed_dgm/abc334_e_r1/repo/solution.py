import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]
    MOD = 998244353
    W2 = W + 2
    # padded grid: 1 = green, 0 = red/border
    g = bytearray((H + 2) * W2)
    for i in range(H):
        r = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if r[j] == 35:  # '#'
                g[base + j] = 1
    lab = [0] * ((H + 2) * W2)
    C = 0
    for s in range(len(g)):
        if g[s] and not lab[s]:
            C += 1
            lab[s] = C
            stack = [s]
            while stack:
                u = stack.pop()
                for v in (u - 1, u + 1, u - W2, u + W2):
                    if g[v] and not lab[v]:
                        lab[v] = C
                        stack.append(v)
    total = 0
    R = 0
    for i in range(1, H + 1):
        base = i * W2
        for u in range(base + 1, base + W + 1):
            if g[u]:
                continue
            R += 1
            a = lab[u - 1]; b = lab[u + 1]; c = lab[u - W2]; d = lab[u + W2]
            k = 0
            seen = []
            for x in (a, b, c, d):
                if x and x not in seen:
                    seen.append(x)
            k = len(seen)
            total += C + 1 - k
    ans = total % MOD * pow(R, MOD - 2, MOD) % MOD
    print(ans)

main()
