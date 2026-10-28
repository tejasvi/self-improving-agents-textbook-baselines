import sys


def main():
    data = sys.stdin.read().split()
    L = int(data[0])
    R = int(data[1])
    res = []
    cur = L
    while cur < R:
        # largest i such that 2^i divides cur and cur + 2^i <= R
        i = 61
        while True:
            p = 1 << i
            if cur % p == 0 and cur + p <= R:
                break
            i -= 1
        p = 1 << i
        res.append((cur, cur + p))
        cur += p
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    sys.stdout.write("\n".join(out) + "\n")


main()
