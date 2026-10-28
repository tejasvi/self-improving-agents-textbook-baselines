import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    # c0, c1: number of starts i <= j with f(i, j) equal to 0 / 1
    c0 = 0
    c1 = 0
    total = 0
    for ch in s:
        if ch == '0':
            # every existing value becomes 1 under NAND with 0
            c1 += c0
            c0 = 0
            # new start with A_j = 0
            c0 += 1
        else:
            # NAND with 1 flips each existing value
            c0, c1 = c1, c0
            # new start with A_j = 1
            c1 += 1
        total += c1
    print(total)


if __name__ == "__main__":
    main()
