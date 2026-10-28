import sys


def main():
    L, R = map(int, sys.stdin.read().split())
    res = []
    l = L
    while l < R:
        if l == 0:
            step = 1 << (R.bit_length() - 1)
        else:
            step = l & (-l)
        while step > R - l:
            step >>= 1
        res.append((l, l + step))
        l += step
    out = [str(len(res))]
    out.extend(f"{a} {b}" for a, b in res)
    print("\n".join(out))


main()
