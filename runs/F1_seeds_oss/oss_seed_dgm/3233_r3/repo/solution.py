class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        # Helper function to compute number of partitions for a given string
        def count_partitions(t: str) -> int:
            partitions = 1  # at least one partition if string is non‑empty
            distinct = set()
            for ch in t:
                if ch not in distinct and len(distinct) == k:
                    # starting a new partition
                    partitions += 1
                    distinct = {ch}
                else:
                    distinct.add(ch)
            return partitions

        n = len(s)
        if n == 0:
            return 0
        # Original number of partitions (no change)
        best = count_partitions(s)
        if k >= 26:
            # All letters are allowed, the whole string is always one partition
            return best

        # Determine for each index the start of the segment (partition) it belongs to
        seg_start = [0] * n
        start = 0
        distinct = set()
        for i, ch in enumerate(s):
            if ch not in distinct and len(distinct) == k:
                # cut before i, so indices start..i-1 belong to previous segment
                for j in range(start, i):
                    seg_start[j] = start
                start = i
                distinct = {ch}
            else:
                distinct.add(ch)
        # fill for the last segment
        for j in range(start, n):
            seg_start[j] = start

        # Try changing each position to a character that is not already present
        # in the prefix of its current segment (if such a character exists).
        for i in range(n):
            seg_begin = seg_start[i]
            # Collect distinct characters that appear before position i in its segment
            before_set = set()
            for j in range(seg_begin, i):
                before_set.add(s[j])
            # Find a replacement character not in before_set
            replacement = None
            for c in (chr(ord('a') + x) for x in range(26)):
                if c not in before_set:
                    replacement = c
                    break
            if replacement is None:
                continue  # cannot introduce a new distinct character here
            if replacement == s[i]:
                continue  # no actual change
            # Build the modified string and evaluate partitions
            modified = s[:i] + replacement + s[i + 1:]
            best = max(best, count_partitions(modified))

        return best
