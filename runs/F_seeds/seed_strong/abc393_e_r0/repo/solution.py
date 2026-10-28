import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    M = max(a)
    freq = [0] * (M + 1)
    for x in a:
        freq[x] += 1
    best = [1] * (M + 1)
    for g in range(1, M + 1):
        c = sum(freq[g::g])
        if c >= k:
            cnt_slots = (M - g) // g + 1
            best[g::g] = [g] * cnt_slots
    sys.stdout.write("\n".join(str(best[x]) for x in a) + "\n")

main()
