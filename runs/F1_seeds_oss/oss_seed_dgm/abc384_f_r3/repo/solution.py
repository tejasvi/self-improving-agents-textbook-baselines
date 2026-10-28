# Write your solution here. Read from stdin, write to stdout.
import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    max_val = max(A)
    max_sum = max_val * 2
    size = max_sum + 1  # length for convolution
    # frequency array
    freq = np.zeros(size, dtype=np.int64)
    for a in A:
        freq[a] += 1
    # perform FFT convolution (ordered pair counts)
    f_fft = np.fft.rfft(freq)
    prod = f_fft * f_fft
    conv = np.fft.irfft(prod, n=size)
    # round to nearest integer
    conv = np.rint(conv).astype(np.int64)
    ans = 0
    # precompute lowbit for each s? compute on the fly
    for s in range(size):
        ordered = conv[s]
        if ordered == 0:
            continue
        diag = freq[s // 2] if (s & 1) == 0 else 0
        unordered = (ordered + diag) // 2
        if unordered == 0:
            continue
        # compute odd part of s (remove all factors of 2)
        # lowbit = s & -s gives largest power of two dividing s
        low = s & -s
        odd = s // low if s != 0 else 0
        ans += unordered * odd
    print(ans)

if __name__ == "__main__":
    main()
