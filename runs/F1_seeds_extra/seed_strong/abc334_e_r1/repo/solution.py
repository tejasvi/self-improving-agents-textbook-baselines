import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
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
    lab = [0] * ((H + 2) * Wp)
    C = 0
    for s in range(len(g)):
        if g[s] and not lab[s]:
            C += 1
            lab[s] = C
            stack = [s]
            while stack:
                v = stack.pop()
                for u in (v - 1, v + 1, v - Wp, v + Wp):
                    if g[u] and not lab[u]:
                        lab[u] = C
                        stack.append(u)
    total = 0
    red = 0
    for i in range(1, H + 1):
        base = i * Wp
        for v in range(base + 1, base + W + 1):
            if not g[v]:
                red += 1
                ls = set()
                a = lab[v - 1]; b = lab[v + 1]; c = lab[v - Wp]; d = lab[v + Wp]
                if a: ls.add(a)
                if b: ls.add(b)
                if c: ls.add(c)
                if d: ls.add(d)
                total += C + 1 - len(ls)
    ans = total % MOD * pow(red, MOD - 2, MOD) % MOD
    print(ans)

main()
