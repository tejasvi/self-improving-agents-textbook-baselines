import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    c0 = 0  # active starts whose current value is 0
    c1 = 0  # active starts whose current value is 1
    ans = 0
    for ch in s:
        if ch == '0':
            # NAND with 0 gives 1 for every active start
            c1 = c0 + c1
            c0 = 0
            c0 += 1  # new start with value 0
        else:
            # NAND with 1 flips every value
            c0, c1 = c1, c0
            c1 += 1  # new start with value 1
        ans += c1
    print(ans)

main()
