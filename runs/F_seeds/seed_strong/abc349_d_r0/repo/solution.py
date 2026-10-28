import sys

def main():
    L, R = map(int, sys.stdin.read().split())
    res = []
    cur = L
    while cur < R:
        size = (cur & -cur) if cur else (1 << 61)
        while cur + size > R:
            size >>= 1
        res.append((cur, cur + size))
        cur += size
    out = [str(len(res))]
    out += ["%d %d" % p for p in res]
    print("\n".join(out))

main()
