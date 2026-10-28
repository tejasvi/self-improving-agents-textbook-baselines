import sys


def main():
    data = sys.stdin.read().split()
    L = int(data[0])
    R = int(data[1])
    res = []
    cur = L
    while cur < R:
        k = 0
        # grow block while aligned and fits
        while True:
            nk = k + 1
            size = 1 << nk
            if cur % size == 0 and cur + size <= R:
                k = nk
            else:
                break
        res.append((cur, cur + (1 << k)))
        cur += 1 << k
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    print("\n".join(out))


main()
