import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    c0 = 0  # number of start indices i <= j whose f(i,j) == 0
    c1 = 0  # ... whose f(i,j) == 1
    total = 0
    for ch in s:
        if ch == '0':
            # every existing value becomes 1 under NAND with 0
            c1 += c0
            c0 = 1  # new start with value 0 (c1 already holds old ones)
        else:
            # NAND with 1 flips every existing value
            c0, c1 = c1, c0
            c1 += 1  # new start with value 1
        total += c1
    print(total)


main()
