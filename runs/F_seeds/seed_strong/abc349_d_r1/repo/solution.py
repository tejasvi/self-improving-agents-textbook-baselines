import sys


def main():
    data = sys.stdin.read().split()
    L, R = int(data[0]), int(data[1])
    res = []
    cur = L
    while cur < R:
        # largest power of two block aligned at cur that fits within R
        k = 0
        while True:
            nk = k + 1
            if cur % (1 << nk) != 0 or cur + (1 << nk) > R:
                break
            k = nk
        size = 1 << k
        res.append((cur, cur + size))
        cur += size
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    print("\n".join(out))


main()
