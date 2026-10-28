import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    maxv = max(A)
    # T[k] = sum over pairs i<=j with 2^k | (A_i+A_j) of (A_i+A_j)
    T = []
    k = 0
    while (1 << k) <= 2 * maxv:
        mask = (1 << k) - 1
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
        mod = 1 << k
        O = 0
        for r, c in cnt.items():
            s = (-r) % mod
            c2 = cnt.get(s)
            if c2:
                O += c * sm[s] + sm[r] * c2
        D = 0
        for a in A:
            if (2 * a) & mask == 0:
                D += 2 * a
        T.append((O + D) // 2)
        k += 1
    T.append(0)
    ans = 0
    for k in range(len(T) - 1):
        E = T[k] - T[k + 1]
        ans += E >> k
    print(ans)


main()
