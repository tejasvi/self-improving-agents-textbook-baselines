from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        """
        Binary search on the answer combined with greedy checking.
        
        For a given minimum score target, we check if we can achieve it with m moves.
        The key insight is:
        - We start at index -1
        - To ensure all indices from 0 to some rightmost index get visited,
          we need to reach that rightmost index
        - We greedily try to reach as far right as possible while ensuring
          all visited indices get at least the target score
        """
        
        def canAchieve(target: int) -> bool:
            """
            Check if we can make all elements have at least 'target' score with m moves.
            We try different rightmost indices and see if any can be achieved with m moves.
            """
            n = len(points)
            
            # Try reaching each possible rightmost index
            for rightmost in range(n):
                # We need to visit all indices from 0 to rightmost
                # and each should accumulate at least 'target' score
                
                # Step 1: Calculate moves to reach rightmost from -1
                moves_to_reach = rightmost + 1
                
                if moves_to_reach > m:
                    continue
                
                remaining_moves = m - moves_to_reach
                
                # Step 2: On the path to rightmost, each index gets visited once
                # So each index i in [0, rightmost] gets points[i]
                
                # Step 3: With remaining moves, we need to accumulate more points
                # Starting from rightmost, we can go back and forth
                
                # Check if each index can reach target
                # By initially going to rightmost, each index [0, rightmost] gets 1 visit
                # We need additional visits for indices that are short of target
                
                visits_needed = []
                for i in range(rightmost + 1):
                    needed = (target + points[i] - 1) // points[i]  # ceil division
                    visits_needed.append(needed)
                
                # With remaining_moves, can we get additional visits?
                # Optimal strategy: go from rightmost to leftmost position that needs more,
                # then oscillate
                
                # Find leftmost index that needs visits > 1
                leftmost_needed = rightmost
                for i in range(rightmost + 1):
                    if visits_needed[i] > 1:
                        leftmost_needed = i
                        break
                
                if visits_needed[rightmost] < 1:
                    # rightmost doesn't need more visits (impossible since visits_needed[i] >= 1)
                    # This won't happen
                    continue
                
                # Cost to go from rightmost to leftmost_needed and back to rightmost
                # and accumulate enough visits for all indices in between
                
                # Greedy: start from rightmost, go left to leftmost_needed
                # Cost: rightmost - leftmost_needed moves
                # Then oscillate between them to get additional visits
                
                cost_to_reach_leftmost = rightmost - leftmost_needed
                if cost_to_reach_leftmost > remaining_moves:
                    continue
                
                remaining_after_reach = remaining_moves - cost_to_reach_leftmost
                
                # Now at leftmost_needed with remaining_after_reach moves
                # We can oscillate between leftmost_needed and rightmost
                # Distance: rightmost - leftmost_needed
                
                if leftmost_needed == rightmost:
                    # Can only oscillate at one position, doesn't add more visits
                    # Actually, we're at rightmost, we can't add more points
                    if visits_needed[rightmost] == 1:
                        return True
                    else:
                        continue
                
                dist = rightmost - leftmost_needed
                
                # Each index from leftmost_needed to rightmost has been visited once
                # On oscillation: if we go right and back (2*dist moves), 
                # each index gets visited 2 more times (plus it's already been visited)
                
                # With remaining_after_reach moves, and distance dist:
                # We can do full_rounds = remaining_after_reach // (2 * dist) full oscillations
                # Plus potentially some partial moves
                
                full_rounds = remaining_after_reach // (2 * dist)
                extra_moves = remaining_after_reach % (2 * dist)
                
                # After full_rounds of oscillations, each index [leftmost_needed, rightmost]
                # gets visited 1 + 2*full_rounds times
                
                valid = True
                for i in range(leftmost_needed, rightmost + 1):
                    visits = 1 + 2 * full_rounds
                    if i == leftmost_needed or i == rightmost:
                        # Endpoints need special handling for extra_moves
                        if extra_moves > 0:
                            if i == rightmost and extra_moves >= (rightmost - leftmost_needed):
                                visits += 1
                            elif i == leftmost_needed and extra_moves > 0:
                                # Coming back from full round, we don't visit leftmost again immediately
                                # unless extra_moves takes us there
                                pass
                    
                    if visits < visits_needed[i]:
                        valid = False
                        break
                
                # Account for extra moves more carefully
                # After full_rounds, we're at rightmost
                # extra_moves allow us to go left up to (rightmost - extra_moves)
                # Each position from (rightmost - extra_moves) to rightmost gets 1 extra visit
                
                if extra_moves > 0:
                    for i in range(rightmost - extra_moves, rightmost + 1):
                        if i >= leftmost_needed:
                            if visits_needed[i] == 1:
                                # Already satisfied from full_rounds
                                continue
                            elif 1 + 2 * full_rounds + 1 >= visits_needed[i]:
                                # Extra move gives us the additional visit
                                continue
                            else:
                                valid = False
                                break
                
                if valid:
                    return True
            
            return False
        
        # Binary search on the answer
        left, right = 0, m * max(points)
        answer = 0
        
        while left <= right:
            mid = (left + right) // 2
            if canAchieve(mid):
                answer = mid
                left = mid + 1
            else:
                right = mid - 1
        
        return answer
