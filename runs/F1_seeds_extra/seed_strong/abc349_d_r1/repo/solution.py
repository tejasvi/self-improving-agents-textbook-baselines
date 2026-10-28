import sys


def main():
    data = sys.stdin.read().split()
    L = int(data[0])
    R = int(data[1])
    res = []
    cur = L
    while cur < R:
        # largest k with cur divisible by 2^k and cur + 2^k <= R
        k = 0
        if cur == 0:
            k = R.bit_length() - 1
        else:
            while (cur >> (k + 1)) << (k + 1) == cur and cur + (1 << (k + 1)) <= R:
                k += 1
        size = 1 << k
        res.append((cur, cur + size))
        cur += size
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    sys.stdout.write("\n".join(out) + "\n")


main()
