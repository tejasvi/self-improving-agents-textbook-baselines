import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    s = list(data[2])
    t = data[3]

    def ok(i):
        has_non_hash = False
        for j in range(m):
            c = s[i + j]
            if c != '#':
                if c != t[j]:
                    return False
                has_non_hash = True
        return has_non_hash

    # Reverse process: repeatedly erase (turn into '#') a window that matches T
    # (with '#' as wildcard). Erasing only creates more matching opportunities,
    # so a greedy stack-based process works.
    stack = [i for i in range(n - m + 1) if ok(i)]
    while stack:
        i = stack.pop()
        if not ok(i):
            continue
        for j in range(m):
            s[i + j] = '#'
        lo = max(0, i - m + 1)
        hi = min(n - m, i + m - 1)
        for k in range(lo, hi + 1):
            if ok(k):
                stack.append(k)

    print("Yes" if all(c == '#' for c in s) else "No")


main()
