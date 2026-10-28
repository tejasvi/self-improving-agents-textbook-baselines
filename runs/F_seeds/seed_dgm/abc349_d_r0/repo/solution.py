import sys


def main():
    data = sys.stdin.read().split()
    L = int(data[0])
    R = int(data[1])
    res = []
    l = L
    while l < R:
        best = 0
        for i in range(62):
            size = 1 << i
            if l % size == 0 and l + size <= R:
                best = i
            else:
                if l % size != 0:
                    break
        size = 1 << best
        res.append((l, l + size))
        l += size
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
