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

    MOD = (1 << 61) - 1
    B = random.randrange(10**5, MOD - 10**5)

    def build(s):
        h = [0] * (len(s) + 1)
        acc = 0
        for idx, ch in enumerate(s.encode()):
            acc = (acc * B + ch) % MOD
            h[idx + 1] = acc
        return h

    HS = build(S)
    HT = build(T)
    maxlen = max(n, m) + 1
    P = [1] * (maxlen + 1)
    for i in range(1, maxlen + 1):
        P[i] = P[i - 1] * B % MOD

    def lcp(i, j):
        # longest common prefix of S[i:] and T[j:]
        hi_lim = min(n - i, m - j)
        lo, hi = 0, hi_lim
        while lo < hi:
            mid = (lo + hi + 1) // 2
            a = (HS[i + mid] - HS[i] * P[mid]) % MOD
            b = (HT[j + mid] - HT[j] * P[mid]) % MOD
            if a == b:
                lo = mid
            else:
                hi = mid - 1
        return lo

    NEG = None
    target = m - n
    # L[d] for current e, d in [-K, K]; index d+K
    prev = [NEG] * (2 * K + 3)
    # e = 0
    off = K + 1
    prev[off + 0] = lcp(0, 0)
    if target == 0 and prev[off + 0] >= n:
        print("Yes")
        return
    for e in range(1, K + 1):
        cur = [NEG] * (2 * K + 3)
        for d in range(-e, e + 1):
            best = None
            # substitution: same diagonal
            pv = prev[off + d]
            if pv is not None:
                cand = pv + 1
                if best is None or cand > best:
                    best = cand
            # insertion in T: from diagonal d-1, i unchanged
            if d - 1 >= -K:
                pv = prev[off + d - 1]
                if pv is not None:
                    cand = pv
                    if best is None or cand > best:
                        best = cand
            # deletion from S: from diagonal d+1, i increases by 1
            if d + 1 <= K:
                pv = prev[off + d + 1]
                if pv is not None:
                    cand = pv + 1
                    if best is None or cand > best:
                        best = cand
            if best is None:
                continue
            i = best
            if i > n:
                i = n
            if i + d > m:
                i = m - d
            if i < 0 or i + d < 0:
                continue
            i += lcp(i, i + d)
            cur[off + d] = i
        if cur[off + target] is not None and cur[off + target] >= n:
            print("Yes")
            return
        prev = cur
    print("No")


main()
