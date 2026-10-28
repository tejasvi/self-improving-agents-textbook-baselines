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
    # best[x] = largest g dividing x such that at least k elements are multiples of g
    best = [1] * (M + 1)
    for g in range(1, M + 1):
        c = sum(freq[g::g])
        if c >= k:
            best[g::g] = [g] * (M // g)  # increasing g, so later (larger) g overwrite
    sys.stdout.write("\n".join(str(best[x]) for x in a) + "\n")

main()
