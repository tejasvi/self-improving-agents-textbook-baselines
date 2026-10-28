import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # prefix counts
    p1 = [0] * (n + 1)
    p2 = [0] * (n + 1)
    for i, ch in enumerate(s, 1):
        p1[i] = p1[i - 1] + (ch == '1')
        p2[i] = p2[i - 1] + (ch == '2')
    slashes = []
    X = []  # ones in [1, m-1]
    Y = []  # twos in [1, m]
    for i, ch in enumerate(s, 1):
        if ch == '/':
            slashes.append(i)
            X.append(p1[i - 1])
            Y.append(p2[i])
    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        lo = bisect_left(slashes, L)
        hi = bisect_right(slashes, R)
        if lo >= hi:
            out.append(0)
            continue
        c1 = p1[L - 1]
        d = p2[R]
        # first k in [lo,hi) with X[k]-c1 >= d-Y[k]
        a, b = lo, hi
        while a < b:
            mid = (a + b) >> 1
            if X[mid] - c1 >= d - Y[mid]:
                b = mid
            else:
                a = mid + 1
        best = 0
        if a < hi:
            v = min(X[a] - c1, d - Y[a])
            if v > best:
                best = v
        if a - 1 >= lo:
            k = a - 1
            v = min(X[k] - c1, d - Y[k])
            if v > best:
                best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
