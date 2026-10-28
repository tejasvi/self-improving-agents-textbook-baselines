import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = sorted(map(int, data[1:1 + n]))
    mid = n // 2
    i = 0
    cnt = 0
    for j in range(mid, n):
        if i < mid and 2 * a[i] <= a[j]:
            i += 1
            cnt += 1
    print(cnt)


main()
