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
    # best[v] = largest g dividing v with count of multiples of g in A >= k
    best = [1] * (m + 1)
    for g in range(1, m + 1):
        c = sum(freq[g::g])
        if c >= k:
            cnt = len(range(g, m + 1, g))
            best[g::g] = [g] * cnt  # increasing g, so final value is max
    sys.stdout.write("\n".join(str(best[x]) for x in a))
    sys.stdout.write("\n")


main()
