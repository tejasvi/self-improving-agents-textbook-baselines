import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]
    Wp = W + 2
    green = bytearray((H + 2) * Wp)
    for i in range(H):
        r = rows[i]
        base = (i + 1) * Wp + 1
        for j in range(W):
            if r[j] == 35:  # '#'
                green[base + j] = 1
    comp = [0] * ((H + 2) * Wp)
    C = 0
    for idx in range(len(green)):
        if green[idx] and not comp[idx]:
            C += 1
            comp[idx] = C
            stack = [idx]
            while stack:
                v = stack.pop()
                for u in (v - 1, v + 1, v - Wp, v + Wp):
                    if green[u] and not comp[u]:
                        comp[u] = C
                        stack.append(u)
    MOD = 998244353
    total = 0
    red = 0
    for i in range(1, H + 1):
        base = i * Wp
        for j in range(1, W + 1):
            idx = base + j
            if green[idx]:
                continue
            red += 1
            a = comp[idx - 1]; b = comp[idx + 1]
            c = comp[idx - Wp]; d = comp[idx + Wp]
            s = set((a, b, c, d))
            s.discard(0)
            total += C - len(s) + 1
    ans = total % MOD * pow(red, MOD - 2, MOD) % MOD
    print(ans)

main()
