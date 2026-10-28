import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    # cnt0/cnt1: number of start indices i <= j whose f(i,j) is 0 / 1.
    cnt0 = 0
    cnt1 = 0
    total = 0
    for j in range(n):
        if s[j] == '0':
            # all existing values become 1; new start has value 0
            cnt1 = j
            cnt0 = 1
        else:
            # existing values flip; new start has value 1
            cnt0, cnt1 = cnt1, cnt0 + 1
        total += cnt1
    print(total)


if __name__ == "__main__":
    main()
