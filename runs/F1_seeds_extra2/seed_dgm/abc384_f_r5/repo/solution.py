import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = np.array(data[1:1 + n], dtype=np.int64)
    maxa = int(a.max())
    m = 2 * maxa  # largest possible sum
    size = 1
    while size < m + 1:
        size *= 2

    c = np.bincount(a, minlength=maxa + 1).astype(np.float64)
    fa = np.fft.rfft(c, size)
    fa *= fa
    conv = np.fft.irfft(fa, size)
    del fa
    ordered = np.rint(conv[:m + 1]).astype(np.int64)
    del conv

    # diagonal: pairs (i,i) with sum 2*A_i
    diag = np.zeros(m + 1, dtype=np.int64)
    cnt_int = np.bincount(a, minlength=maxa + 1).astype(np.int64)
    diag[0:2 * maxa + 1:2] = cnt_int[:maxa + 1]

    pairs = (ordered + diag) // 2  # unordered pairs i <= j with sum s
    s = np.arange(1, m + 1, dtype=np.int64)
    odd = s // (s & -s)  # f(s)
    ans = int(np.sum(pairs[1:] * odd))
    print(ans)


main()
