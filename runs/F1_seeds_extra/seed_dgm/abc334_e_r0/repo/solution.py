import sys


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    MOD = 998244353
    W2 = W + 2
    N = (H + 2) * W2
    green = bytearray(N)
    for i in range(H):
        row = data[2 + i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if row[j] == 35:  # '#'
                green[base + j] = 1

    label = [0] * N
    C = 0
    for start in range(N):
        if green[start] and not label[start]:
            C += 1
            label[start] = C
            stack = [start]
            pop = stack.pop
            push = stack.append
            while stack:
                v = pop()
                for u in (v - 1, v + 1, v - W2, v + W2):
                    if green[u] and not label[u]:
                        label[u] = C
                        push(u)

    total = 0
    red_count = 0
    for i in range(1, H + 1):
        base = i * W2
        for j in range(1, W + 1):
            v = base + j
            if green[v]:
                continue
            red_count += 1
            seen = set()
            for u in (v - 1, v + 1, v - W2, v + W2):
                l = label[u]
                if l:
                    seen.add(l)
            total += C + 1 - len(seen)

    ans = total % MOD * pow(red_count % MOD, MOD - 2, MOD) % MOD
    print(ans)


main()
