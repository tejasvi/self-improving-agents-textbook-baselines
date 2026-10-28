# Solution for 11/22 Subsequence problem
import sys, bisect

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    S = next(it).strip()
    # 1-indexed prefix sums
    pref1 = [0] * (N + 1)
    pref2 = [0] * (N + 1)
    slash_pos = []  # positions (1-indexed) where S[i-1]=='/'
    for i, ch in enumerate(S, start=1):
        pref1[i] = pref1[i-1] + (1 if ch == '1' else 0)
        pref2[i] = pref2[i-1] + (1 if ch == '2' else 0)
        if ch == '/':
            slash_pos.append(i)
    out_lines = []
    for _ in range(Q):
        L = int(next(it))
        R = int(next(it))
        # find slashes within [L,R]
        lo = bisect.bisect_left(slash_pos, L)
        hi = bisect.bisect_right(slash_pos, R) - 1
        if lo > hi:
            out_lines.append('0')
            continue
        total1_before = pref1[L-1]
        total2_up_to_R = pref2[R]
        # helper to compute diff = x - y for a given index in slash_pos list
        def diff_at(idx):
            pos = slash_pos[idx]
            x = pref1[pos-1] - total1_before
            y = total2_up_to_R - pref2[pos]
            return x - y
        # binary search first index where diff > 0
        left, right = lo, hi
        pos_gt = hi + 1  # default none
        while left <= right:
            mid = (left + right) // 2
            if diff_at(mid) > 0:
                pos_gt = mid
                right = mid - 1
            else:
                left = mid + 1
        if pos_gt == lo:
            # all diffs > 0, min is y at lo
            pos = slash_pos[lo]
            k = total2_up_to_R - pref2[pos]
            out_lines.append(str(2 * k + 1))
        elif pos_gt == hi + 1:
            # all diffs <= 0, min is x at hi
            pos = slash_pos[hi]
            k = pref1[pos-1] - total1_before
            out_lines.append(str(2 * k + 1))
        else:
            # crossing point between pos_gt-1 and pos_gt
            # candidate from left side (min = x)
            pos_left = slash_pos[pos_gt - 1]
            k1 = pref1[pos_left-1] - total1_before
            # candidate from right side (min = y)
            pos_right = slash_pos[pos_gt]
            k2 = total2_up_to_R - pref2[pos_right]
            k = k1 if k1 >= k2 else k2
            out_lines.append(str(2 * k + 1))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
