import sys


def main():
    data = sys.stdin.read().split()
    L = int(data[0])
    R = int(data[1])
    res = []
    l = L
    while l < R:
        if l == 0:
            size = 1 << 61
        else:
            size = l & (-l)  # largest power of two dividing l
        while l + size > R:
            size >>= 1
        res.append((l, l + size))
        l += size
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
