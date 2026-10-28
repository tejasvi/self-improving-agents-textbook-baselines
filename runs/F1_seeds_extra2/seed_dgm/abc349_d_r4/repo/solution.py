import sys


def main():
    data = sys.stdin.read().split()
    L, R = int(data[0]), int(data[1])
    res = []
    l = L
    while l < R:
        # largest power of two block starting at l, aligned, fitting in R
        i = 60
        while True:
            size = 1 << i
            if l % size == 0 and l + size <= R:
                break
            i -= 1
        res.append((l, l + (1 << i)))
        l += 1 << i
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
