import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1]); q = int(data[2])
    S = [0] * m; T = [0] * m
    pos = 3
    for i in range(m):
        s = int(data[pos]); t = int(data[pos + 1]); pos += 2
        S[i] = s; T[i] = t
    size = 1
    while size < n + 2:
        size *= 2
    NEG = 0          # max-tree identity (b >= 2 always, so 0 means absent)
    POS = 1 << 30    # min-tree identity
    # For direction d: MAXB[d] indexed by a (left endpoint) stores b (max tree)
    #                  MINA[d] indexed by b (right endpoint) stores a (min tree)
    MAXB = [[NEG] * (2 * size) for _ in range(2)]
    MINA = [[POS] * (2 * size) for _ in range(2)]
    cntA = [0] * (n + 2)
    cntB = [0] * (n + 2)

    A = [0] * m; B = [0] * m; D = [0] * m
    for i in range(m):
        s = S[i]; t = T[i]
        if s < t:
            A[i] = s; B[i] = t; D[i] = 0
        else:
            A[i] = t; B[i] = s; D[i] = 1

    def set_pos(d, a, b):
        # MAXB: index a -> value b ; MINA: index b -> value a
        tr = MAXB[d]
        i = a + size
        tr[i] = b if b is not None else NEG
        i >>= 1
        while i:
            x = tr[2 * i]; y = tr[2 * i + 1]
            tr[i] = x if x > y else y
            i >>= 1
        tr2 = MINA[d]
        j = b + size
        tr2[j] = a if a is not None else POS
        j >>= 1
        while j:
            x = tr2[2 * j]; y = tr2[2 * j + 1]
            tr2[j] = x if x < y else y
            j >>= 1

    def can_add(j):
        a = A[j]; b = B[j]; d = D[j]
        if cntA[a] or cntB[b]:
            return False
        # conflict2: exists existing (a', b') with a' in (a,b), b' > b
        lo = a + 1 + size; hi = b - 1 + size + 1  # half-open [lo, hi)
        tr = MAXB[d]
        mx = NEG
        while lo < hi:
            if lo & 1:
                if tr[lo] > mx: mx = tr[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                if tr[hi] > mx: mx = tr[hi]
            lo >>= 1; hi >>= 1
        if mx > b:
            return False
        # conflict1: exists existing (a', b') with b' in (a,b), a' < a
        lo = a + 1 + size; hi = b + size
        tr2 = MINA[d]
        mn = POS
        while lo < hi:
            if lo & 1:
                if tr2[lo] < mn: mn = tr2[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                if tr2[hi] < mn: mn = tr2[hi]
            lo >>= 1; hi >>= 1
        if mn < a:
            return False
        return True

    # two pointers: ans_r[l] = exclusive end r such that [l, r) is conflict-free maximal
    ans_r = [0] * m
    r = 0
    for l in range(m):
        while r < m and can_add(r):
            a = A[r]; b = B[r]; d = D[r]
            cntA[a] += 1; cntB[b] += 1
            set_pos(d, a, b)
            r += 1
        ans_r[l] = r
        # remove l
        a = A[l]; b = B[l]; d = D[l]
        cntA[a] -= 1; cntB[b] -= 1
        tr = MAXB[d]
        i = a + size
        tr[i] = NEG
        i >>= 1
        while i:
            x = tr[2 * i]; y = tr[2 * i + 1]
            tr[i] = x if x > y else y
            i >>= 1
        tr2 = MINA[d]
        j = b + size
        tr2[j] = POS
        j >>= 1
        while j:
            x = tr2[2 * j]; y = tr2[2 * j + 1]
            tr2[j] = x if x < y else y
            j >>= 1

    out = []
    for _ in range(q):
        L = int(data[pos]) - 1; R = int(data[pos + 1]) - 1; pos += 2
        out.append("Yes" if R < ans_r[L] else "No")
    sys.stdout.write("\n".join(out) + "\n")

main()
