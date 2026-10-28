import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    P = [int(x) for x in data[2:2 + n]]

    def add(t, i, d):
        while i <= n:
            t[i] += d
            i += i & -i

    def pref(t, i):  # count of inserted values <= i
        s = 0
        while i > 0:
            s += t[i]
            i -= i & -i
        return s

    # total inversions of P
    bit = [0] * (n + 1)
    total_inv = 0
    for p in range(n):
        v = P[p]
        total_inv += p - pref(bit, v)
        add(bit, v, 1)

    M = n - k + 1

    # I_W: inversions inside the sliding window
    bit = [0] * (n + 1)
    I_in = 0
    for j in range(k):
        v = P[j]
        I_in += j - pref(bit, v)  # j elements inserted so far, all in window
        add(bit, v, 1)

    sum_I = I_in
    for i in range(1, M):
        # remove P[i-1] (leftmost, so it is the first element of window)
        x = P[i - 1]
        # inversions involving x inside window: elements after it that are smaller
        smaller_in_window = pref(bit, x - 1)
        I_in -= smaller_in_window
        add(bit, x, -1)
        # add P[i+k-1] (rightmost): inversions with window elements larger than it
        y = P[i + k - 1]
        size = k - 1
        larger_in_window = size - pref(bit, y)
        I_in += larger_in_window
        add(bit, y, 1)
        sum_I += I_in

    # E = (1/M) * sum_i (total_inv - I_i + C(k,2)/2)
    inv2 = pow(2, MOD - 2, MOD)
    half_pairs = (k * (k - 1) // 2) % MOD * inv2 % MOD
    numer = (M * total_inv - sum_I + M * half_pairs) % MOD
    ans = numer * pow(M, MOD - 2, MOD) % MOD
    print(ans)


main()
