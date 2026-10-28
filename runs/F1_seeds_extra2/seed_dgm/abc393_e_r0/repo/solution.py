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
    # cnt[g] = number of elements divisible by g
    # best[v] = max good g dividing v (good: cnt[g] >= k); g=1 is always good
    best = [1] * (m + 1)
    for g in range(1, m + 1):
        c = sum(freq[g::g])
        if c >= k:
            # ascending order: later (larger) g overwrite, giving the max
            best[g::g] = [g] * len(range(g, m + 1, g))
    sys.stdout.write("\n".join(str(best[x]) for x in a))
    sys.stdout.write("\n")

main()
