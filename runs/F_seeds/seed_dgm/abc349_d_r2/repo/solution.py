import sys


def main():
    L, R = map(int, sys.stdin.read().split())
    res = []
    l = L
    while l < R:
        for i in range(61, -1, -1):
            step = 1 << i
            if l % step == 0 and l + step <= R:
                res.append((l, l + step))
                l += step
                break
    out = [str(len(res))]
    out += [f"{a} {b}" for a, b in res]
    print("\n".join(out))


main()
