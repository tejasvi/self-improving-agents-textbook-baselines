import sys


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    MOD = 998244353
    rows = data[2:2 + H]
    W2 = W + 2
    # padded grid: green[idx] = True if green
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
        if green[s] and label[s] == 0:
            C += 1
            label[s] = C
            stack = [s]
            pop = stack.pop
            push = stack.append
            while stack:
                v = pop()
                for u in (v - 1, v + 1, v - W2, v + W2):
                    if green[u] and label[u] == 0:
                        label[u] = C
                        push(u)

    total = 0
    red = 0
    for i in range(H):
        base = (i + 1) * W2 + 1
        for j in range(W):
            p = base + j
            if green[p]:
                continue
            red += 1
            a = label[p - 1]
            b = label[p + 1]
            c = label[p - W2]
            d = label[p + W2]
            k = 0
            seen = []
            for x in (a, b, c, d):
                if x and x not in seen:
                    seen.append(x)
            k = len(seen)
            total += C + 1 - k

    ans = total % MOD * pow(red, MOD - 2, MOD) % MOD
    print(ans)


main()
