import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); K = int(data[1])
    A = list(map(int, data[2:2 + n]))
    M = max(A)
    freq = [0] * (M + 1)
    for a in A:
        freq[a] += 1
    # cnt[d] = number of elements divisible by d
    cnt = [0] * (M + 1)
    for d in range(1, M + 1):
        cnt[d] = sum(freq[d::d])
    # g[m] = largest d dividing m with cnt[d] >= K
    g = [0] * (M + 1)
    for d in range(1, M + 1):
        if cnt[d] >= K:
            g[d::d] = [d] * len(range(d, M + 1, d))
    sys.stdout.write('\n'.join([str(g[a]) for a in A]) + '\n')

main()
