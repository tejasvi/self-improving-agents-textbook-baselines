import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    s = list(data[2])
    t = data[3]

    def ok(p):
        allq = True
        for j in range(m):
            c = s[p + j]
            if c != '?':
                allq = False
                if c != t[j]:
                    return False
        return not allq

    q = deque(p for p in range(n - m + 1) if ok(p))
    while q:
        p = q.popleft()
        if not ok(p):
            continue
        for j in range(m):
            s[p + j] = '?'
        lo = max(0, p - m + 1)
        hi = min(n - m, p + m - 1)
        for r in range(lo, hi + 1):
            if ok(r):
                q.append(r)

    print("Yes" if all(c == '?' for c in s) else "No")


main()
