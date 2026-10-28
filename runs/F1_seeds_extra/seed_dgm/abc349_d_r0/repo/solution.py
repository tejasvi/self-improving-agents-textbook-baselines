import sys


def main():
    data = sys.stdin.read().split()
    L, R = int(data[0]), int(data[1])
    res = []
    cur = L
    while cur < R:
        # largest power of two block starting at cur that is aligned and fits
        i = 0
        while i < 61 and cur % (1 << (i + 1)) == 0 and cur + (1 << (i + 1)) <= R:
            i += 1
        size = 1 << i
        res.append((cur, cur + size))
        cur += size
    out = [str(len(res))]
    for l, r in res:
        out.append(f"{l} {r}")
    print("\n".join(out))


main()
