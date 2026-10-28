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
        row = rows[i]
        base = (i + 1) * W2 + 1
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
            while stack:
                v = stack.pop()
                for u in (v - 1, v + 1, v - W2, v + W2):
                    if green[u] and not label[u]:
                        label[u] = C
                        stack.append(u)
    R = 0
    sumk = 0
    for i in range(H):
        base = (i + 1) * W2 + 1
        for j in range(W):
            v = base + j
            if not green[v]:
                R += 1
                a = label[v - 1]
                b = label[v + 1]
                c = label[v - W2]
                d = label[v + W2]
                # count distinct nonzero labels
                k = 0
                if a:
                    k = 1
                    if b and b != a:
                        k += 1
                    if c and c != a and c != b:
                        k += 1
                    if d and d != a and d != b and d != c:
                        k += 1
                else:
                    if b:
                        k = 1
                        if c and c != b:
                            k += 1
                        if d and d != b and d != c:
                            k += 1
                    elif c:
                        k = 1
                        if d and d != c:
                            k += 1
                    elif d:
                        k = 1
                sumk += k
    total = R * (C + 1) - sumk
    ans = total % MOD * pow(R % MOD, MOD - 2, MOD) % MOD
    print(ans)

main()
