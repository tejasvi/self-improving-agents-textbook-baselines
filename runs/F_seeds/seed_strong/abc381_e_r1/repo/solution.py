import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # prefix counts: P1[i] = number of '1' in s[1..i], P2 similarly
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
    pos = []
    A = []  # ones before slash: P1[m-1]
    B = []  # twos after slash: P2[N]-P2[m] handled via P2[m]
    K = []
    for i, ch in enumerate(s, 1):
        if ch == '/':
            pos.append(i)
            a = P1[i - 1]
            b = P2[i]
            A.append(a)
            B.append(b)
            K.append(a + b)
    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx])
        R = int(data[idx + 1])
        idx += 2
        lo = bisect_left(pos, L)
        hi = bisect_right(pos, R)
        if lo >= hi:
            out.append(0)
            continue
        x = P1[L - 1]
        y = P2[R]
        t = bisect_right(K, x + y, lo, hi)
        best = 0
        if t - 1 >= lo:
            i = t - 1
            v = min(A[i] - x, y - B[i])
            if v > best:
                best = v
        if t < hi:
            i = t
            v = min(A[i] - x, y - B[i])
            if v > best:
                best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
