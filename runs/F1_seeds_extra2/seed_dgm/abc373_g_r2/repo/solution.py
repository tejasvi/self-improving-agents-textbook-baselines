import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:]))
    pts = []
    for i in range(n):
        pts.append((vals[2 * i], vals[2 * i + 1], 0, i))
    for j in range(n):
        k = 2 * n + 2 * j
        pts.append((vals[k], vals[k + 1], 1, j))

    ans = [0] * n
    # Divide and conquer: take the lowest point of the current set, sort the
    # rest by polar angle around it, and match it with the first opposite-type
    # point at which the prefix is balanced. This splits the set into two
    # independent balanced halves, so segments never cross.
    stack = [pts]
    while stack:
        cur = stack.pop()
        if not cur:
            continue
        best = 0
        for i in range(1, len(cur)):
            if (cur[i][1], cur[i][0]) < (cur[best][1], cur[best][0]):
                best = i
        p = cur[best]
        others = cur[:best] + cur[best + 1:]
        px, py = p[0], p[1]
        # All other points lie in the upper half-plane (or on the right ray), angles in [0, pi).
        others.sort(key=lambda q: math.atan2(q[1] - py, q[0] - px))
        s = p[2]
        cnt = 0
        match_idx = -1
        for k, q in enumerate(others):
            if q[2] == s:
                cnt += 1
            else:
                if cnt == 0:
                    match_idx = k
                    break
                cnt -= 1
        q = others[match_idx]
        if p[2] == 0:
            ans[p[3]] = q[3]
        else:
            ans[q[3]] = p[3]
        stack.append(others[:match_idx])
        stack.append(others[match_idx + 1:])
    print(" ".join(str(x + 1) for x in ans))


main()
