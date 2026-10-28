import sys


def main():
    data = sys.stdin.read().split()
    L = int(data[0])
    R = int(data[1])
    res = []
    l = L
    while l < R:
        # largest i such that l is divisible by 2^i and l + 2^i <= R
        i = 0
        while i < 61 and (l % (1 << (i + 1)) == 0 or l == 0) and l + (1 << (i + 1)) <= R:
            i += 1
        r = l + (1 << i)
        res.append((l, r))
        l = r
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
