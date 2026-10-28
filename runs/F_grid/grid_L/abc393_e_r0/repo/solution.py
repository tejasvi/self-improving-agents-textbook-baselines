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
    best = [1] * (m + 1)
    for d in range(1, m + 1):
        c = sum(freq[d::d])
        if c >= k:
            # d is a qualifying divisor; larger d processed later overwrite
            best[d::d] = [d] * len(range(d, m + 1, d))
    out = [best[x] for x in a]
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
