import sys


def main():
    data = sys.stdin.read().split()
    L, R = int(data[0]), int(data[1])
    pieces = []
    l = L
    while l < R:
        # largest i such that 2^i divides l and l + 2^i <= R
        i = 0
        while i < 61 and (l % (1 << (i + 1)) == 0 or l == 0) and l + (1 << (i + 1)) <= R:
            i += 1
        pieces.append((l, l + (1 << i)))
        l += 1 << i
    out = [str(len(pieces))]
    for a, b in pieces:
        out.append(f"{a} {b}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
