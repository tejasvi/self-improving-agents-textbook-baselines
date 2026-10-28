import sys
import random


def main():
    data = sys.stdin.read().split()
    K = int(data[0])
    S = data[1]
    T = data[2]
    n = len(S)
    m = len(T)

    if abs(n - m) > K:
        print("No")
        return

    # Polynomial rolling hash modulo 2^61 - 1.
    MOD = (1 << 61) - 1
    B = random.randrange(10**6, MOD - 10**6)
    N = max(n, m) + 1
    pw = [1] * (N + 1)
    for i in range(1, N + 1):
        pw[i] = pw[i - 1] * B % MOD

    def prefix(s, length):
        h = [0] * (length + 1)
        cur = 0
        for i, c in enumerate(s.encode()):
            cur = (cur * B + c) % MOD
            h[i + 1] = cur
        return h

    hs = prefix(S, n)
    ht = prefix(T, m)

    def sub(h, l, r):
        return (h[r] - h[l] * pw[r - l]) % MOD

    def lce(i, j):
        # longest common prefix of S[i:] and T[j:]
        hi_lim = min(n - i, m - j)
        lo, hi = 0, hi_lim
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if sub(hs, i, i + mid) == sub(ht, j, j + mid):
                lo = mid
            else:
                hi = mid - 1
        return lo

    NEG = -(10 ** 9)

    def valid(i, k):
        return 0 <= i <= n and 0 <= i + k <= m

    # prev[k + K] = furthest row on diagonal k with d-1 edits (k = j - i)
    OFF = K + 1
    size = 2 * K + 3
    prev = [NEG] * size

    # d = 0
    i0 = lce(0, 0)
    prev[OFF] = i0
    target_k = m - n
    if prev[OFF] == n and target_k == 0:
        print("Yes")
        return

    for d in range(1, K + 1):
        cur = [NEG] * size
        for k in range(-d, d + 1):
            idx = k + OFF
            best = NEG
            # substitution: from diagonal k, (i+1, j+1)
            p = prev[idx]
            if p > NEG:
                best = max(best, p + 1)
            # insertion into S (j advances): from diagonal k-1, same i
            p = prev[idx - 1]
            if p > NEG:
                best = max(best, p)
            # deletion from S (i advances): from diagonal k+1, i+1
            p = prev[idx + 1]
            if p > NEG:
                best = max(best, p + 1)
            if best <= NEG:
                continue
            i = best
            # clip to grid
            if i > n:
                i = n
            if i + k > m:
                i = m - k
            if not valid(i, k):
                continue
            i += lce(i, i + k)
            cur[idx] = i
        if cur[target_k + OFF] == n:
            print("Yes")
            return
        prev = cur

    print("No")


main()
