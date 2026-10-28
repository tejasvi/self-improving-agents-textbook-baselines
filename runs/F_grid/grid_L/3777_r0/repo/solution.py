from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        bound = 12 * n  # |alternating sum| never exceeds this
        if abs(k) > bound:
            return -1

        # Part 1: can a subsequence containing a zero have alternating sum k?
        # State: (parity of length, alt sum, has_zero) -> reachable (booleans).
        reach = {(0, 0, 0)}  # parity 0 == empty subsequence so far
        for x in nums:
            new = set(reach)
            for (p, s, z) in reach:
                ns = s + x if p == 0 else s - x
                new.add((1 - p, ns, z or (x == 0)))
            reach = new
        zero_ok = any(s == k and z == 1 for (p, s, z) in reach)

        # Part 2: non-empty subsequences of nonzero elements with products <= limit.
        # State: (parity, alt sum) -> set of achievable products (<= limit).
        # Parity 0 with sum 0 denotes the empty subsequence (no product yet).
        best = -1
        dp = {(0, 0): {1}}  # product 1 for the empty subsequence
        for x in nums:
            if x == 0:
                continue
            new = {key: set(vals) for key, vals in dp.items()}
            for (p, s), prods in dp.items():
                ns = s + x if p == 0 else s - x
                key = (1 - p, ns)
                target = new.setdefault(key, set())
                for pr in prods:
                    np_ = pr * x
                    if np_ <= limit:
                        target.add(np_)
            dp = {key: v for key, v in new.items() if v}
        # Non-empty: the empty subsequence has parity 0 and sum 0 with product 1;
        # a non-empty subsequence with parity 1 ends after odd count; ending with
        # parity 0 and sum k is non-empty only if k != 0 or it has elements.
        # Simplest correct handling: check parity-1 states (always non-empty)
        # and parity-0 states with non-empty content tracked via a flag below.
        cand = dp.get((1, k))
        if cand:
            best = max(cand)
        # Parity-0 states with sum k that are non-empty (even length >= 2).
        # Those are tracked by a second DP that excludes the empty start.
        dp2 = {}
        for x in nums:
            if x == 0:
                continue
            new = {key: set(vals) for key, vals in dp2.items()}
            # start a new subsequence with x
            new.setdefault((1, x), set())
            if x <= limit:
                new[(1, x)].add(x)
            for (p, s), prods in dp2.items():
                ns = s + x if p == 0 else s - x
                target = new.setdefault((1 - p, ns), set())
                for pr in prods:
                    np_ = pr * x
                    if np_ <= limit:
                        target.add(np_)
            dp2 = {key: v for key, v in new.items() if v}
        cand = dp2.get((0, k))
        if cand:
            best = max(best, max(cand))

        if zero_ok:
            best = max(best, 0)
        return best
