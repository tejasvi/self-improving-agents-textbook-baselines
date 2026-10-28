# Write your solution here. Read from stdin, write to stdout.

import sys
import bisect

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    S = next(it).strip()
    # 1-indexed prefix sums for '1' and '2'
    prefix1 = [0] * (N + 1)
    prefix2 = [0] * (N + 1)
    slash_pos = []  # positions (1-indexed) where character is '/'
    for i, ch in enumerate(S, start=1):
        prefix1[i] = prefix1[i-1] + (1 if ch == '1' else 0)
        prefix2[i] = prefix2[i-1] + (1 if ch == '2' else 0)
        if ch == '/':
            slash_pos.append(i)
    out_lines = []
    for _ in range(Q):
        L = int(next(it))
        R = int(next(it))
        # find slashes within [L, R]
        l_idx = bisect.bisect_left(slash_pos, L)
        r_idx = bisect.bisect_right(slash_pos, R) - 1
        if l_idx > r_idx:
            out_lines.append('0')
            continue
        # helper to compute min count for a slash at index idx in slash_pos list
        def min_cnt(idx):
            p = slash_pos[idx]
            cnt1 = prefix1[p-1] - prefix1[L-1]
            cnt2 = prefix2[R] - prefix2[p]
            return cnt1 if cnt1 < cnt2 else cnt2
        # binary search for first position where cnt1 >= cnt2
        low, high = l_idx, r_idx
        while low < high:
            mid = (low + high) // 2
            p = slash_pos[mid]
            cnt1 = prefix1[p-1] - prefix1[L-1]
            cnt2 = prefix2[R] - prefix2[p]
            if cnt1 < cnt2:
                low = mid + 1
            else:
                high = mid
        best = min_cnt(low)
        if low - 1 >= l_idx:
            cand = min_cnt(low - 1)
            if cand > best:
                best = cand
        # length of longest 11/22 subsequence
        ans = 2 * best + 1
        out_lines.append(str(ans))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
