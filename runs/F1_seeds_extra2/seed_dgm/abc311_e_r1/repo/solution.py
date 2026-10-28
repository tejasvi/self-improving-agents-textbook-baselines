import sys


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    holes = [[] for _ in range(H)]
    p = 3
    for _ in range(N):
        a = int(data[p]) - 1
        b = int(data[p + 1]) - 1
        holes[a].append(b)
        p += 2

    D = [0] * W          # down run length from current row
    S_prev = [0] * (W + 1)  # largest square top-left at (i+1, j), index W is sentinel 0
    total = 0
    for i in range(H - 1, -1, -1):
        hs = sorted(holes[i])
        free = [True] * W
        for b in hs:
            free[b] = False
        # down run lengths
        D = [d + 1 if f else 0 for d, f in zip(D, free)]
        # right run lengths
        R = [0] * W
        start = 0
        for b in hs + [W]:
            seg = b - start
            if seg > 0:
                R[start:b] = range(seg, 0, -1)
            start = b + 1
        # S(i+1, j+1) + 1
        shifted = [x + 1 for x in S_prev[1:]]
        S = list(map(min, R, D, shifted))
        for b in hs:
            S[b] = 0
        total += sum(S)
        S_prev = S + [0]
    print(total)


main()
