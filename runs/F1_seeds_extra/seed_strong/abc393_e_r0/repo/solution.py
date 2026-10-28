import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    V = max(a)
    cnt = [0] * (V + 1)
    for x in a:
        cnt[x] += 1
    # best[v] = largest g dividing v with M(g) >= k
    best = [1] * (V + 1)
    for g in range(1, V + 1):
        if sum(cnt[g::g]) >= k:
            best[g::g] = [g] * len(range(g, V + 1, g))
    out = [best[x] for x in a]
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
