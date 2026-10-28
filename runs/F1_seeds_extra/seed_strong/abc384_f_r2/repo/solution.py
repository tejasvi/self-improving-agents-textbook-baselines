import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    maxs = 2 * max(A)
    E = []
    for k in range(26):
        if (1 << k) > maxs:
            E.append(0)
            continue
        M = 1 << k
        mask = M - 1
        cnt = {}
        sm = {}
        for a in A:
            r = a & mask
            if r in cnt:
                cnt[r] += 1
                sm[r] += a
            else:
                cnt[r] = 1
                sm[r] = a
        ordered = 0
        for r, c in cnt.items():
            cb = cnt.get((-r) & mask)
            if cb:
                ordered += sm[r] * cb + c * sm[(-r) & mask]
        diag = 0
        for a in A:
            if (2 * a) & mask == 0:
                diag += 2 * a
        E.append((ordered + diag) // 2)
    E.append(0)
    ans = 0
    for k in range(26):
        ans += (E[k] - E[k + 1]) >> k
    print(ans)


main()
