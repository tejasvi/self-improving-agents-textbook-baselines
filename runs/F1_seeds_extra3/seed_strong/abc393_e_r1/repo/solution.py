import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    M = max(a)
    cnt = [0] * (M + 1)
    for x in a:
        cnt[x] += 1
    # c[d] = number of elements divisible by d
    good = [False] * (M + 1)
    for d in range(1, M + 1):
        if sum(cnt[d::d]) >= k:
            good[d] = True
    # best[v] = largest good d dividing v (0 if none)
    best = [0] * (M + 1)
    for d in range(1, M + 1):
        if good[d]:
            best[d::d] = [d] * len(range(d, M + 1, d))
    sys.stdout.write("\n".join(str(best[x]) for x in a) + "\n")

main()
