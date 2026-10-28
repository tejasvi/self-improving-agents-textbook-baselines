import sys


def main():
    L, R = map(int, sys.stdin.read().split())
    res = []
    l = L
    while l < R:
        # largest power of two p such that p divides l (or any p if l == 0) and l + p <= R
        cap = (l & -l) if l else (1 << 62)
        p = 1
        while p * 2 <= cap and l + p * 2 <= R:
            p *= 2
        res.append((l, l + p))
        l += p
    out = [str(len(res))]
    for a, b in res:
        out.append(f"{a} {b}")
    print("\n".join(out))


main()
