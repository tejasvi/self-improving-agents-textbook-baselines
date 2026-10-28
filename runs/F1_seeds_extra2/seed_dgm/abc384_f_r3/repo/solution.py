import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    maxs = 2 * max(a)
    # T[v] = sum of (A_i + A_j) over pairs i <= j with 2^v | (A_i + A_j)
    T = []
    v = 0
    while True:
        M = 1 << v
        if M > maxs:
            T.append(0)
            break
        cnt = {}
        sm = {}
        for x in a:
            r = x & (M - 1)
            if r in cnt:
                cnt[r] += 1
                sm[r] += x
            else:
                cnt[r] = 1
                sm[r] = x
        total = 0
        for r, c in cnt.items():
            p = (M - r) & (M - 1)
            if r == p:
                total += (c + 1) * sm[r]
            elif r < p and p in cnt:
                total += c * sm[p] + cnt[p] * sm[r]
        T.append(total)
        v += 1
    T.append(0)
    ans = 0
    for v in range(len(T) - 1):
        d = T[v] - T[v + 1]
        ans += d >> v
    print(ans)


main()
