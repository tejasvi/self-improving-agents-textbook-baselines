import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    M = max(a)
    freq = [0] * (M + 1)
    for x in a:
        freq[x] += 1
    # cnt[g] = number of elements divisible by g
    best = [1] * (M + 1)
    for g in range(1, M + 1):
        if sum(freq[g::g]) >= k:
            # every multiple of g gets candidate g; increasing g so largest wins
            best[g::g] = [g] * len(range(g, M + 1, g))
    sys.stdout.write("\n".join(str(best[x]) for x in a) + "\n")

main()
