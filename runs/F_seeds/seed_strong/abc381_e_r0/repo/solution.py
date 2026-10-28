import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
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
    # prevSl[i]: largest '/' index <= i (0 if none); nextSl[i]: smallest '/' index >= i (n+1 if none)
    prevSl = [0] * (n + 2)
    last = 0
    for i in range(1, n + 1):
        if s[i - 1] == '/':
            last = i
        prevSl[i] = last
    nextSl = [n + 1] * (n + 2)
    nxt = n + 1
    for i in range(n, 0, -1):
        if s[i - 1] == '/':
            nxt = i
        nextSl[i] = nxt

    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx])
        R = int(data[idx + 1])
        idx += 2
        # any slash in [L, R]?
        f = nextSl[L]
        if f > R:
            out.append(0)
            continue
        C = P1[L - 1] + P2[R]
        # g(m) = P1[m-1] + P2[m] nondecreasing; find largest m in [L,R] with g(m) <= C
        lo, hi = L - 1, R + 1
        # invariant: g(lo) <= C (lo = L-1 treated as true), g(hi+1) > C (treated)
        while hi - lo > 1:
            mid = (lo + hi) >> 1
            if P1[mid - 1] + P2[mid] <= C:
                lo = mid
            else:
                hi = mid
        p = lo  # in [L-1, R]
        best = 0
        if p >= L:
            m1 = prevSl[p]
            if m1 >= L:
                ones = P1[m1 - 1] - P1[L - 1]
                twos = P2[R] - P2[m1]
                v = ones if ones < twos else twos
                if v > best:
                    best = v
        if p + 1 <= R:
            m2 = nextSl[p + 1]
            if m2 <= R:
                ones = P1[m2 - 1] - P1[L - 1]
                twos = P2[R] - P2[m2]
                v = ones if ones < twos else twos
                if v > best:
                    best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
