import sys

def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    A = list(map(int, data[2:2 + n]))
    M = max(A)
    freq = [0] * (M + 1)
    for a in A:
        freq[a] += 1
    best = [1] * (M + 1)
    # cnt[g] = number of elements divisible by g; ascending g so larger good g overwrite
    for g in range(1, M + 1):
        if sum(freq[g::g]) >= k:
            best[g::g] = [g] * (M // g)
    sys.stdout.write('\n'.join([str(best[a]) for a in A]) + '\n')

main()
