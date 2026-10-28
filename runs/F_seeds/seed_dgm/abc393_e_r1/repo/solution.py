import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    M = max(a)
    f = [0] * (M + 1)
    for v in a:
        f[v] += 1
    # best[x] = largest g dividing x with cnt[g] >= k (0 if none)
    best = [0] * (M + 1)
    for g in range(1, M + 1):
        c = sum(f[g::g])
        if c >= k:
            best[g::g] = [g] * len(range(g, M + 1, g))
    out = [best[v] for v in a]
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
