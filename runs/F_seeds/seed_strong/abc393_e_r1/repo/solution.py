import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    M = max(a)
    cnt = [0] * (M + 1)
    for v in a:
        cnt[v] += 1
    # best[v] = largest g dividing v with at least k multiples in A
    best = [1] * (M + 1)
    for g in range(1, M + 1):
        c = sum(cnt[g::g])
        if c >= k:
            L = len(range(g, M + 1, g))
            best[g::g] = [g] * L
    sys.stdout.write("\n".join(str(best[v]) for v in a) + "\n")

main()
