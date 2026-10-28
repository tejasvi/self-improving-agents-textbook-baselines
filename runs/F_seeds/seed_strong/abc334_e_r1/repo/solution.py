import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    MOD = 998244353
    Wp = W + 2
    N = (H + 2) * Wp
    green = bytearray(N)
    for i in range(H):
        row = data[2 + i]
        base = (i + 1) * Wp + 1
        for j in range(W):
            if row[j] == 35:  # '#'
                green[base + j] = 1
    label = [0] * N
    C = 0
    for s in range(N):
        if green[s] and not label[s]:
            C += 1
            label[s] = C
            stack = [s]
            pop = stack.pop; push = stack.append
            while stack:
                v = pop()
                for u in (v - 1, v + 1, v - Wp, v + Wp):
                    if green[u] and not label[u]:
                        label[u] = C
                        push(u)
    total = 0
    R = 0
    for i in range(1, H + 1):
        base = i * Wp
        for v in range(base + 1, base + W + 1):
            if not green[v]:
                R += 1
                a = label[v - 1]; b = label[v + 1]; c = label[v - Wp]; d = label[v + Wp]
                k = len({a, b, c, d} - {0})
                total += C + 1 - k
    ans = total % MOD * pow(R % MOD, MOD - 2, MOD) % MOD
    print(ans)

main()
