import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(data[1 + 2 * i]) for i in range(n)]
    B = [int(data[2 + 2 * i]) for i in range(n)]
    adj = [0] * n
    for i in range(n):
        for j in range(n):
            if i != j and (A[i] == A[j] or B[i] == B[j]):
                adj[i] |= 1 << j
    # win[mask]: player to move wins with remaining cards = mask.
    # Masks only decrease numerically when cards are removed, so ascending order works.
    full = (1 << n) - 1
    win = bytearray(1 << n)  # 0 = losing, 1 = winning
    for mask in range(1, 1 << n):
        # enumerate cards in mask that have a neighbor in mask
        m = mask
        res = 0
        while m:
            low = m & -m
            i = low.bit_length() - 1
            m ^= low
            nb = adj[i] & mask
            while nb:
                lj = nb & -nb
                nb ^= lj
                if not win[mask ^ low ^ lj]:
                    res = 1
                    break
            if res:
                break
        win[mask] = res
    print("Takahashi" if win[full] else "Aoki")


main()
