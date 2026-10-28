import sys


def main():
    data = sys.stdin.read().split()
    L, R = int(data[0]), int(data[1])
    res = []
    cur = L
    while cur < R:
        # largest power of two block aligned at cur that fits in [cur, R)
        i = 0
        while i + 1 <= 61 and cur % (1 << (i + 1)) == 0 and cur + (1 << (i + 1)) <= R:
            i += 1
        res.append((cur, cur + (1 << i)))
        cur += 1 << i
    out = [str(len(res))]
    out += [f"{a} {b}" for a, b in res]
    print("\n".join(out))


main()
