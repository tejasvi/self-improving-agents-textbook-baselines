import sys


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    rows = data[2:2 + H]
    MOD = 998244353
    Wp = W + 2
    N = (H + 2) * Wp
    green = bytearray(N)
    for i in range(H):
        row = rows[i]
        base = (i + 1) * Wp + 1
        for j in range(W):
            if row[j] == 35:  # '#'
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
                p = pop()
                for q in (p - 1, p + 1, p - Wp, p + Wp):
                    if green[q] and comp[q] == 0:
                        comp[q] = C
                        push(q)

    total = 0
    R = 0
    for i in range(1, H + 1):
        base = i * Wp
        for p in range(base + 1, base + W + 1):
            if green[p]:
                continue
            R += 1
            a = comp[p - 1]
            b = comp[p + 1]
            c = comp[p - Wp]
            d = comp[p + Wp]
            # count distinct nonzero values
            distinct = 0
            seen = []
            for v in (a, b, c, d):
                if v and v not in seen:
                    seen.append(v)
            distinct = len(seen)
            total += C + 1 - distinct

    ans = total % MOD * pow(R, MOD - 2, MOD) % MOD
    print(ans)


main()
