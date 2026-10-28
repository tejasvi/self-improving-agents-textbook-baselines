import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]
    MOD = 998244353
    W2 = W + 2
    N = (H + 2) * W2
    green = bytearray(N)
    for i in range(H):
        r = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if r[j] == 35:  # '#'
                green[base + j] = 1
    comp = [0] * N
    C = 0
    for s in range(N):
        if green[s] and comp[s] == 0:
            C += 1
            comp[s] = C
            stack = [s]
            pop = stack.pop
            push = stack.append
            while stack:
                v = pop()
                for u in (v - 1, v + 1, v - W2, v + W2):
                    if green[u] and comp[u] == 0:
                        comp[u] = C
                        push(u)
    R = 0
    sumk = 0
    for i in range(1, H + 1):
        base = i * W2
        for v in range(base + 1, base + W + 1):
            if not green[v]:
                R += 1
                a = comp[v - 1]; b = comp[v + 1]; c = comp[v - W2]; d = comp[v + W2]
                k = 0
                if a: k += 1
                if b and b != a: k += 1
                if c and c != a and c != b: k += 1
                if d and d != a and d != b and d != c: k += 1
                sumk += k
    total = R * (C + 1) - sumk
    ans = total % MOD * pow(R, MOD - 2, MOD) % MOD
    print(ans)

main()
