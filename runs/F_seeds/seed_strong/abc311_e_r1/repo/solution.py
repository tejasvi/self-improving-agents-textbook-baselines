import sys
from itertools import accumulate


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    holes = [[] for _ in range(H + 1)]
    idx = 3
    for _ in range(N):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        holes[a].append(b - 1)
    # v[j] = cur[j] - j, where cur[j] = largest holeless square ending at (i, j)
    # cur[j] = min(prev[j], prev[j-1], cur[j-1]) + 1 (0 if holed)
    # => v[j] = min(vprev[j] + 1, vprev[j-1], v[j-1]) with holes giving v[j] = -j
    base = list(range(0, -W, -1))  # row above grid: cur = 0 -> v[j] = -j
    vp = base
    total = 0
    sum_idx = W * (W - 1) // 2
    for i in range(1, H + 1):
        left = [1] + vp[:-1]  # vprev[j-1], with vprev[-1] = 1 (cur[-1] = 0)
        w = list(map(min, map((1).__add__, vp), left))
        for b in holes[i]:
            w[b] = -b
        v = list(accumulate(w, min))
        total += sum(v) + sum_idx
        vp = v
    print(total)


main()
