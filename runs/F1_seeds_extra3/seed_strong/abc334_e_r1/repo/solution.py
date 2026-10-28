import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]
    MOD = 998244353
    W2 = W + 2
    # padded grid: green = 1, border = 0
    green = bytearray((H + 2) * W2)
    for i in range(H):
        r = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if r[j] == 35:  # '#'
                green[base + j] = 1
    comp = [0] * ((H + 2) * W2)
    C = 0
    for s in range(len(green)):
        if green[s] and not comp[s]:
            C += 1
            comp[s] = C
            stack = [s]
            while stack:
                v = stack.pop()
                for u in (v - 1, v + 1, v - W2, v + W2):
                    if green[u] and not comp[u]:
                        comp[u] = C
                        stack.append(u)
    R = 0
    sumk = 0
    for i in range(1, H + 1):
        base = i * W2
        for v in range(base + 1, base + W + 1):
            if not green[v]:
                R += 1
                a = comp[v - 1]; b = comp[v + 1]; c = comp[v - W2]; d = comp[v + W2]
                k = 0
                seen = []
                for x in (a, b, c, d):
                    if x and x not in seen:
                        seen.append(x)
                sumk += len(seen)
    num = (R * (C + 1) - sumk) % MOD
    print(num * pow(R, MOD - 2, MOD) % MOD)

main()
