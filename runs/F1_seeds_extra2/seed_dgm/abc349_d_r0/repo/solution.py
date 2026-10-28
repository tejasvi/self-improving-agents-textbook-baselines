import sys


def main():
    data = sys.stdin.read().split()
    L = int(data[0])
    R = int(data[1])
    res = []
    cur = L
    while cur < R:
        for k in range(61, -1, -1):
            step = 1 << k
            if cur % step == 0 and cur + step <= R:
                res.append((cur, cur + step))
                cur += step
                break
    out = [str(len(res))]
    for l, r in res:
        out.append(f"{l} {r}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
