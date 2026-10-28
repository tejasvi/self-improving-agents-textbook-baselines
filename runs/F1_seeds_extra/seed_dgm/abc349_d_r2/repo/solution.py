import sys


def main():
    data = sys.stdin.read().split()
    L = int(data[0])
    R = int(data[1])
    res = []
    cur = L
    while cur < R:
        # largest i with 2^i dividing cur (cur=0 -> unbounded, limited by R)
        i = 0
        while True:
            nxt = i + 1
            if nxt > 62:
                break
            size = 1 << nxt
            if cur % size != 0 or cur + size > R:
                break
            i = nxt
        size = 1 << i
        res.append((cur, cur + size))
        cur += size
    out = [str(len(res))]
    for l, r in res:
        out.append(f"{l} {r}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
