import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    m = max(a)
    cnt = [0] * (m + 1)
    for x in a:
        cnt[x] += 1
    best = [1] * (m + 1)
    for d in range(1, m + 1):
        # number of elements divisible by d
        if sum(cnt[d::d]) >= k:
            # ascending order: later (larger) d overwrite earlier ones
            best[d::d] = [d] * len(range(d, m + 1, d))
    sys.stdout.write("\n".join(str(best[x]) for x in a))
    sys.stdout.write("\n")


main()
