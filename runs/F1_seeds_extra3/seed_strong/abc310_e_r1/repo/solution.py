import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    # c0, c1: counts of starts i<=j whose current NAND-fold value is 0 / 1
    c0 = 0
    c1 = 0
    total = 0
    for ch in s:
        if ch == '0':
            c1 += c0
            c0 = 1
        else:
            c0, c1 = c1, c0
            c1 += 1
        total += c1
    print(total)


if __name__ == "__main__":
    main()
