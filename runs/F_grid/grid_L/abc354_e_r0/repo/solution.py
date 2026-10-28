import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(data[1 + 2 * i]) for i in range(n)]
    b = [int(data[2 + 2 * i]) for i in range(n)]

    adj = [0] * n
    for i in range(n):
        for j in range(n):
            if i != j and (a[i] == a[j] or b[i] == b[j]):
                adj[i] |= 1 << j

    sys.setrecursionlimit(10000)
    memo = {}

    # win(mask): the player to move wins with the remaining cards in mask.
    def win(mask):
        r = memo.get(mask)
        if r is not None:
            return r
        res = False
        m = mask
        while m and not res:
            low = m & -m
            i = low.bit_length() - 1
            m ^= low
            nb = adj[i] & mask & ~((low << 1) - 1)  # neighbors j > i
            while nb:
                lj = nb & -nb
                nb ^= lj
                if not win(mask ^ low ^ lj):
                    res = True
                    break
        memo[mask] = res
        return res

    full = (1 << n) - 1
    print("Takahashi" if win(full) else "Aoki")


main()
