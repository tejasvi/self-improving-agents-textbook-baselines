import sys

def main():
    data = sys.stdin.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]
    W2 = W + 2
    N = (H + 2) * W2
    green = bytearray(N)
    for i in range(H):
        row = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if row[j] == '#':
                green[base + j] = 1

    label = [0] * N
    C = 0
    offs = (1, -1, W2, -W2)
    for i in range(H):
        base = (i + 1) * W2 + 1
        for j in range(W):
            s = base + j
            if green[s] and not label[s]:
                C += 1
                label[s] = C
                stack = [s]
                while stack:
                    u = stack.pop()
                    for d in offs:
                        v = u + d
                        if green[v] and not label[v]:
                            label[v] = C
                            stack.append(v)

    total = 0
    R = 0
    for i in range(H):
        base = (i + 1) * W2 + 1
        for j in range(W):
            s = base + j
            if green[s]:
                continue
            R += 1
            a = label[s - 1]
            b = label[s + 1]
            c = label[s - W2]
            d = label[s + W2]
            k = 0
            seen = []
            for x in (a, b, c, d):
                if x and x not in seen:
                    seen.append(x)
            k = len(seen)
            total += C - k + 1

    MOD = 998244353
    ans = total % MOD * pow(R, MOD - 2, MOD) % MOD
    print(ans)

main()
