import sys


def main():
    data = sys.stdin.read().split()
    L = int(data[0])
    R = int(data[1])
    res = []
    cur = L
    while cur < R:
        # largest i such that cur is divisible by 2^i and cur + 2^i <= R
        i = 60
        while i > 0 and (cur & ((1 << i) - 1) or cur + (1 << i) > R):
            i -= 1
        nxt = cur + (1 << i)
        res.append((cur, nxt))
        cur = nxt
    out = [str(len(res))]
    for l, r in res:
        out.append(f"{l} {r}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
