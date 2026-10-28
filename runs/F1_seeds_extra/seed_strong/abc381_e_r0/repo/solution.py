import sys
def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    s = data[2].decode()
    # 1-indexed prefix counts
    P1 = [0] * (n + 1)
    P2 = [0] * (n + 1)
    c1 = c2 = 0
    for i, ch in enumerate(s, 1):
        if ch == '1':
            c1 += 1
        elif ch == '2':
            c2 += 1
        P1[i] = c1
        P2[i] = c2
    # nextS[i]: first slash position >= i (or n+1); prevS[i]: last slash position <= i (or 0)
    nextS = [n + 1] * (n + 2)
    for i in range(n, 0, -1):
        nextS[i] = i if s[i - 1] == '/' else nextS[i + 1]
    prevS = [0] * (n + 2)
    for i in range(1, n + 1):
        prevS[i] = i if s[i - 1] == '/' else prevS[i - 1]
    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        ns = nextS[L]
        if ns > R:
            out.append(0)
            continue
        x = P1[L - 1]
        y = P2[R]
        # smallest p in [L,R] with P1[p-1]-x >= y-P2[p]; R+1 if none
        lo, hi = L, R + 1
        while lo < hi:
            mid = (lo + hi) >> 1
            if P1[mid - 1] - x >= y - P2[mid]:
                hi = mid
            else:
                lo = mid + 1
        p = lo
        best = 0
        if p <= R:
            m = nextS[p]
            if m <= R:
                k = min(P1[m - 1] - x, y - P2[m])
                if k > best:
                    best = k
        if p - 1 >= L:
            m = prevS[p - 1]
            if m >= L:
                k = min(P1[m - 1] - x, y - P2[m])
                if k > best:
                    best = k
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")
main()
