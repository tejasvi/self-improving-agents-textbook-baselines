import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    M = max(a)
    freq = [0] * (M + 1)
    for x in a:
        freq[x] += 1
    # best[x] = largest g dividing x with cnt[g] >= k (cnt[g] = #elements divisible by g)
    best = [1] * (M + 1)
    for g in range(1, M + 1):
        c = sum(freq[g::g])
        if c >= k:
            cnt_m = (M - g) // g + 1
            best[g::g] = [g] * cnt_m
    out = [str(best[x]) for x in a]
    sys.stdout.write("\n".join(out) + "\n")

main()
