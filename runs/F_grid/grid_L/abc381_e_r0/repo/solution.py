import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # 1-indexed prefix counts
    p1 = [0] * (n + 1)
    p2 = [0] * (n + 1)
    for i, ch in enumerate(s, 1):
        p1[i] = p1[i - 1] + (ch == '1')
        p2[i] = p2[i - 1] + (ch == '2')
    # prev_slash[x]: largest slash index <= x (0 if none)
    # next_slash[x]: smallest slash index >= x (n+1 if none)
    prev_slash = [0] * (n + 2)
    for i, ch in enumerate(s, 1):
        prev_slash[i] = i if ch == '/' else prev_slash[i - 1]
    next_slash = [n + 1] * (n + 2)
    for i in range(n, 0, -1):
        next_slash[i] = i if s[i - 1] == '/' else next_slash[i + 1]

    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx])
        R = int(data[idx + 1])
        idx += 2
        # smallest p in [L,R] with ones in [L,p) >= twos in (p,R]
        lo, hi = L, R + 1
        base1 = p1[L - 1]
        totalTwo = p2[R]
        while lo < hi:
            mid = (lo + hi) >> 1
            f = p1[mid - 1] - base1
            g = totalTwo - p2[mid]
            if f >= g:
                hi = mid
            else:
                lo = mid + 1
        p0 = lo
        best = 0
        cands = []
        if p0 - 1 >= L:
            m = prev_slash[p0 - 1]
            if m >= L:
                cands.append(m)
        if p0 <= R:
            m = next_slash[p0]
            if m <= R:
                cands.append(m)
        for m in cands:
            f = p1[m - 1] - base1
            g = totalTwo - p2[m]
            v = 2 * min(f, g) + 1
            if v > best:
                best = v
        out.append(best)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
