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
    # cnt[g] = number of elements divisible by g
    cnt = [0] * (m + 1)
    for g in range(1, m + 1):
        cnt[g] = sum(freq[g::g])
    # ans[v] = largest g dividing v with cnt[g] >= k (g=1 always works since k<=n)
    ans = [1] * (m + 1)
    for g in range(1, m + 1):
        if cnt[g] >= k:
            length = m // g
            ans[g::g] = [g] * length
    sys.stdout.write('\n'.join(str(ans[x]) for x in a) + '\n')


main()
