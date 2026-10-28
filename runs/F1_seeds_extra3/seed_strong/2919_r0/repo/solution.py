from typing import *


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Sort ascending; greedily open group k+1 (size k+1) once the
        # accumulated capacity covers sizes 1..k+1, i.e. (k+1)(k+2)/2.
        total = 0
        k = 0
        for x in sorted(usageLimits):
            total += x
            need = (k + 1) * (k + 2) // 2
            if total >= need:
                k += 1
        return k
