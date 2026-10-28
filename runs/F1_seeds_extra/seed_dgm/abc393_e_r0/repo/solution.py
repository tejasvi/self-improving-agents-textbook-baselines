import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    m = max(a)

    freq = [0] * (m + 1)
    for x in a:
        freq[x] += 1

    # best[v] = largest d dividing v with cnt[d] >= k (d = 1 always qualifies)
    best = [1] * (m + 1)
    for d in range(1, m + 1):
        c = sum(freq[d::d])
        if c >= k:
            cnt = len(range(d, m + 1, d))
            best[d::d] = [d] * cnt

    out = [best[x] for x in a]
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
