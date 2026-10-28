import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    Q = int(data[idx]); idx += 1

    Ls = [0] * (M + 1)
    Hs = [0] * (M + 1)
    Ds = [0] * (M + 1)  # 1 if rightward (T > S), else 0
    for i in range(1, M + 1):
        s = int(data[idx]); t = int(data[idx + 1]); idx += 2
        if s < t:
            Ls[i] = s; Hs[i] = t; Ds[i] = 1
        else:
            Ls[i] = t; Hs[i] = s; Ds[i] = 0

    size = 1
    while size < N + 2:
        size <<= 1
    INF = 1 << 30
    minT = [[INF] * (2 * size) for _ in range(2)]
    maxT = [[-INF] * (2 * size) for _ in range(2)]
    cntL = [0] * (N + 2)
    cntR = [0] * (N + 2)

    def set_min(t, pos, val):
        p = pos + size
        t[p] = val
        p >>= 1
        while p:
            a = t[2 * p]; b = t[2 * p + 1]
            t[p] = a if a < b else b
            p >>= 1

    def set_max(t, pos, val):
        p = pos + size
        t[p] = val
        p >>= 1
        while p:
            a = t[2 * p]; b = t[2 * p + 1]
            t[p] = a if a > b else b
            p >>= 1

    def query_min(t, lo, hi):  # inclusive
        res = INF
        lo += size; hi += size + 1
        while lo < hi:
            if lo & 1:
                if t[lo] < res: res = t[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                if t[hi] < res: res = t[hi]
            lo >>= 1; hi >>= 1
        return res

    def query_max(t, lo, hi):  # inclusive
        res = -INF
        lo += size; hi += size + 1
        while lo < hi:
            if lo & 1:
                if t[lo] > res: res = t[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                if t[hi] > res: res = t[hi]
            lo >>= 1; hi >>= 1
        return res

    def can_add(j):
        l = Ls[j]; h = Hs[j]
        if cntL[l] or cntR[h]:
            return False
        d = Ds[j]
        if l + 1 <= h - 1:
            # same-direction i with l_i < l < h_i < h
            if query_min(minT[d], l + 1, h - 1) < l:
                return False
            # same-direction i with l < l_i < h < h_i
            if query_max(maxT[d], l + 1, h - 1) > h:
                return False
        return True

    def add(j):
        l = Ls[j]; h = Hs[j]; d = Ds[j]
        cntL[l] += 1
        cntR[h] += 1
        set_min(minT[d], h, l)
        set_max(maxT[d], l, h)

    def remove(j):
        l = Ls[j]; h = Hs[j]; d = Ds[j]
        cntL[l] -= 1
        cntR[h] -= 1
        set_min(minT[d], h, INF)
        set_max(maxT[d], l, -INF)

    lo_of = [1] * (M + 1)
    lo = 1
    for r in range(1, M + 1):
        while not can_add(r):
            remove(lo)
            lo += 1
        add(r)
        lo_of[r] = lo

    out = []
    for _ in range(Q):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        out.append("Yes" if L >= lo_of[R] else "No")
    sys.stdout.write("\n".join(out) + "\n")


main()
