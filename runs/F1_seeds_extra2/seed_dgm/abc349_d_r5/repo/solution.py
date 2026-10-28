import sys


def main():
    data = sys.stdin.read().split()
    L, R = int(data[0]), int(data[1])
    res = []
    l = L
    while l < R:
        # largest i such that 2^i divides l (l==0 -> unlimited) and l + 2^i <= R
        i = 61
        while True:
            size = 1 << i
            if (l % size == 0) and l + size <= R:
                break
            i -= 1
        r = l + (1 << i)
        res.append((l, r))
        l = r
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    sys.stdout.write("\n".join(out) + "\n")


main()
