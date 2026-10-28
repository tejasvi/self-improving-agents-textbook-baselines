import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    M = max(a)
    freq = [0] * (M + 1)
    for x in a:
        freq[x] += 1
    # cnt[g] = number of elements divisible by g
    cnt = [0] * (M + 1)
    for g in range(1, M + 1):
        cnt[g] = sum(freq[g::g])
    # best[v] = largest divisor g of v with cnt[g] >= k (ascending g, later overwrite)
    best = [1] * (M + 1)
    for g in range(1, M + 1):
        if cnt[g] >= k:
            L = len(range(g, M + 1, g))
            best[g::g] = [g] * L
    out = [str(best[x]) for x in a]
    sys.stdout.write("\n".join(out) + "\n")


main()
