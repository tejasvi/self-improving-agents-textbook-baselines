import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    c0 = 0  # number of starts i<=j with f(i,j)=0
    c1 = 0  # number of starts i<=j with f(i,j)=1
    ans = 0
    for ch in s:
        if ch == '0':
            # all earlier starts become 1; new start has value 0
            c1 = c0 + c1
            c0 = 1
        else:
            # NAND with 1 flips every earlier value; new start has value 1
            c0, c1 = c1, c0
            c1 += 1
        ans += c1
    print(ans)


main()
