import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # prefix counts (1-indexed): P1[i] = number of '1' in s[1..i]
    P1 = [0] * (n + 1)
    P2 = [0] * (n + 1)
    slashes = []
    c1 = c2 = 0
    for i, ch in enumerate(s, 1):
        if ch == '1':
            c1 += 1
        elif ch == '2':
            c2 += 1
        else:
            slashes.append(i)
        P1[i] = c1
        P2[i] = c2
    ns = len(slashes)
    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx])
        R = int(data[idx + 1])
        idx += 2
        # slash indices within [L, R]
        lo = _lower(slashes, L)
        hi = _lower(slashes, R + 1)
        if lo >= hi:
            out.append(0)
            continue
        base1 = P1[L - 1]
        totalTwo = P2[R]
        # A(i) = ones in [L, m-1], B(i) = twos in [m+1, R], increasing/decreasing in i
        a, b = lo, hi
        while a < b:
            mid = (a + b) >> 1
            m = slashes[mid]
            A = P1[m - 1] - base1
            B = totalTwo - P2[m]
            if A > B:
                b = mid
            else:
                a = mid + 1
        best = 0
        j = a
        if j < hi:
            m = slashes[j]
            A = P1[m - 1] - base1
            B = totalTwo - P2[m]
            v = A if A < B else B
            if v > best:
                best = v
        if j - 1 >= lo:
            m = slashes[j - 1]
            A = P1[m - 1] - base1
            B = totalTwo - P2[m]
            v = A if A < B else B
            if v > best:
                best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


def _lower(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) >> 1
        if arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


main()
