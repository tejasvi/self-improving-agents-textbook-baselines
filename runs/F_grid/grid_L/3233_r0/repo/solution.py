class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        # DP over left-to-right greedy simulation.
        # State: segment mask -> max number of completed cuts.
        # Two families: unchanged (no change used yet) and changed (change used).
        bits = [1 << (ord(ch) - 97) for ch in s]
        n = len(s)

        def step(states, b):
            new = {}
            for mask, cnt in states.items():
                if mask & b or bin(mask).count("1") < k:
                    nm, nc = mask | b, cnt
                else:
                    nm, nc = b, cnt + 1
                if new.get(nm, -1) < nc:
                    new[nm] = nc
            return new

        def merge(dst, src):
            for m, c in src.items():
                if dst.get(m, -1) < c:
                    dst[m] = c

        unchanged = {0: 0}
        changed = {}
        for i in range(n):
            b = bits[i]
            nxt_changed = step(changed, b) if changed else {}
            # use the change at position i: any letter x
            if unchanged:
                from_change = {}
                for x in range(26):
                    merge(from_change, step(unchanged, 1 << x))
                merge(nxt_changed, from_change)
            unchanged = step(unchanged, b) if unchanged else {}
            changed = nxt_changed
        best = 0
        for states in (unchanged, changed):
            for mask, cnt in states.items():
                best = max(best, cnt + 1)
        return best
