import sys


def main():
    data = sys.stdin.read().split()
    L, R = int(data[0]), int(data[1])
    res = []
    cur = L
    while cur < R:
        size = 1 << ((R - cur).bit_length() - 1)
        while cur % size != 0:
            size >>= 1
        res.append((cur, cur + size))
        cur += size
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    sys.stdout.write("\n".join(out) + "\n")


main()
