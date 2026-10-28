import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()[:n]
    c0 = 0  # number of start indices i with f(i,j) == 0
    c1 = 0  # number of start indices i with f(i,j) == 1
    total = 0
    ans = 0
    for ch in s:
        total += 1
        if ch == '0':
            # x NAND 0 = 1 for all existing; new start gives 0
            c1 = total - 1
            c0 = 1
        else:
            # x NAND 1 = NOT x: swap counts; new start gives 1
            c0, c1 = c1, c0
            c1 += 1
        ans += c1
    print(ans)


if __name__ == "__main__":
    main()
