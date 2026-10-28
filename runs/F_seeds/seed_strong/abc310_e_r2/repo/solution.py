import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    # c0, c1: number of starting indices i (<= j) whose current f(i,j) is 0 / 1
    c0 = 0
    c1 = 0
    total = 0
    for ch in s:
        if ch == '0':
            # NAND with 0 gives 1 for every existing start; new start has value 0
            c1 = c0 + c1
            c0 = 1
        else:
            # NAND with 1 flips every existing value; new start has value 1
            c0, c1 = c1, c0
            c1 += 1
        total += c1
    print(total)


if __name__ == "__main__":
    main()
