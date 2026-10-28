# Write your solution here. Read from stdin, write to stdout.
import sys

def odd_part(x: int) -> int:
    # Return x with all factors of 2 removed.
    # Using lowest set bit trick: x // (x & -x)
    return x // (x & -x)

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    A = [int(next(it)) for _ in range(n)]
    # diagonal contribution: sum f(A_i) because f(2*A_i)=f(A_i)
    diag = sum(odd_part(a) for a in A)
    max_sum = max(A) * 2
    max_t = max_sum.bit_length()  # enough bits to cover up to max_sum
    total_all = 0
    # Pre‑compute A list for faster access
    for t in range(max_t):
        mod = 1 << (t + 1)
        mask = mod - 1
        target = 1 << t
        # build residue counts
        cnt = {}
        for a in A:
            r = a & mask
            cnt[r] = cnt.get(r, 0) + 1
        prod_sum = 0
        for a in A:
            r = a & mask
            need = (target - r) & mask
            c = cnt.get(need, 0)
            prod_sum += a * c
        ordered_sum = prod_sum * 2  # sum of (A_i + A_j) over ordered pairs
        total_all += ordered_sum >> t
    answer = (total_all + diag) // 2
    print(answer)

if __name__ == "__main__":
    solve()
