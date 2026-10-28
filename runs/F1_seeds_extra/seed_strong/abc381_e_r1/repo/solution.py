import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    s = data[2].decode()
    # prefix counts, 1-indexed: o[i] = #'1' in S[1..i], t[i] = #'2' in S[1..i]
    o = [0] * (n + 1)
    t = [0] * (n + 1)
    slashes = []
    co = 0; ct = 0
    for i, ch in enumerate(s, 1):
        if ch == '1':
            co += 1
        elif ch == '2':
            ct += 1
        else:
            slashes.append(i)
        o[i] = co
        t[i] = ct
    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        lo = bisect_left(slashes, L)
        hi = bisect_right(slashes, R)
        if lo >= hi:
            out.append(0)
            continue
        oL = o[L - 1]
        tR = t[R]
        # diff(p) = (o[p-1]-oL) - (tR - t[p]) is nondecreasing in p
        a, b = lo, hi
        while a < b:
            m = (a + b) >> 1
            p = slashes[m]
            if (o[p - 1] - oL) - (tR - t[p]) >= 0:
                b = m
            else:
                a = m + 1
        j = a
        best = 0
        if j - 1 >= lo:
            p = slashes[j - 1]
            k = min(o[p - 1] - oL, tR - t[p])
            if k > best:
                best = k
        if j < hi:
            p = slashes[j]
            k = min(o[p - 1] - oL, tR - t[p])
            if k > best:
                best = k
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
