import sys


def main():
    L, R = map(int, sys.stdin.read().split())
    res = []
    l = L
    while l < R:
        # largest i with l divisible by 2^i and l + 2^i <= R
        i = 0
        while True:
            nxt = i + 1
            if nxt > 61:
                break
            step = 1 << nxt
            if l % step != 0 or l + step > R:
                break
            i = nxt
        r = l + (1 << i)
        res.append((l, r))
        l = r
    out = [str(len(res))]
    out += [f"{a} {b}" for a, b in res]
    print("\n".join(out))


main()
