import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # prefix counts (1-indexed): c1[i] = #'1' in s[1..i], c2[i] = #'2' in s[1..i]
    c1 = [0] * (n + 1)
    c2 = [0] * (n + 1)
    a = b = 0
    slash_pos = []
    for i, ch in enumerate(s, 1):
        if ch == '1':
            a += 1
        elif ch == '2':
            b += 1
        else:
            slash_pos.append(i)
        c1[i] = a
        c2[i] = b
    # For slash at m: A = c1[m], B = c2[m], K = A + B (nondecreasing in m)
    A = [c1[m] for m in slash_pos]
    B = [c2[m] for m in slash_pos]
    K = [A[j] + B[j] for j in range(len(slash_pos))]
    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        lo = bisect_left(slash_pos, L)
        hi = bisect_right(slash_pos, R) - 1
        if lo > hi:
            out.append(0)
            continue
        p = c1[L - 1]
        qq = c2[R]
        j = bisect_left(K, p + qq, lo, hi + 1)
        best = 0
        if j <= hi:
            v = qq - B[j]
            if v > best:
                best = v
        if j - 1 >= lo:
            v = A[j - 1] - p
            if v > best:
                best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
