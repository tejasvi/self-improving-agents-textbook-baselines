import sys


def main():
    data = sys.stdin.read().split()
    L = int(data[0])
    R = int(data[1])
    res = []
    l = L
    while l < R:
        # largest power of two block starting at l that stays within R
        best = 0
        for i in range(61, -1, -1):
            size = 1 << i
            if l % size == 0 and l + size <= R:
                best = size
                break
        res.append((l, l + best))
        l += best
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
