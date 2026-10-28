import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    a = data[2:2 + n]
    pos = 2 + n
    queries_by_r = [[] for _ in range(n + 1)]
    for i in range(q):
        r = int(data[pos])
        x = int(data[pos + 1])
        pos += 2
        queries_by_r[r].append((i, x))

    ans = [0] * q
    tails = []
    for r in range(1, n + 1):
        v = int(a[r - 1])
        k = bisect_left(tails, v)
        if k == len(tails):
            tails.append(v)
        else:
            tails[k] = v
        for idx, x in queries_by_r[r]:
            ans[idx] = bisect_right(tails, x)

    sys.stdout.write("\n".join(map(str, ans)) + ("\n" if q else ""))


main()
