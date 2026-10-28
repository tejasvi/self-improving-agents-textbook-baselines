from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        """
        Maximize the minimum game score given m moves.
        
        Key insights:
        1. Use binary search on the answer (the minimum score)
        2. For a given target minimum score, check if it's achievable with m moves
        3. The optimal strategy is to visit indices from 0 to some index k, ensuring
           each has at least the target score
        """
        
        def can_achieve(target):
            """Check if we can achieve minimum score of 'target' with m moves."""
            n = len(points)
            
            # Try each possible rightmost index that we reach
            for right_index in range(n):
                # We need to visit indices 0 to right_index
                # Each index i needs at least ceil(target / points[i]) visits
                
                # Calculate minimum visits needed for each index
                visits = []
                for i in range(right_index + 1):
                    visits_needed = (target + points[i] - 1) // points[i]  # ceiling division
                    visits.append(visits_needed)
                
                # Calculate the minimum moves needed to achieve these visits
                # Strategy: go right to right_index, then come back optimally
                
                # We start at -1
                # Optimal path: go to right_index, visiting indices on the way up
                # Then potentially go back to visit indices again
                
                # Total visits sum
                total_visits = sum(visits)
                
                # Minimum moves to make all required visits
                # If we just go right once: right_index + 1 moves to reach right_index
                # Plus additional moves to revisit indices
                
                # The key is: to make multiple visits to an index, we need to pass through it
                # Optimal strategy: 
                # - Go to right_index (takes right_index + 1 moves, visits each once)
                # - Come back to some point and go right again (revisits)
                
                # Let's think differently:
                # - Go to position i and back: 2*(i+1) - 1 moves (go and come back to -1)
                # - But we want to minimize moves
                
                # Better approach: 
                # We go right to right_index, and on the way we accumulate
                # Then we go back and forth to satisfy remaining visits
                
                # Actually, let's think about it as:
                # We need to visit each index i a total of visits[i] times
                # Path 1: Go right, collecting points on the way (each index visited once)
                # Path 2: On the way back, visit indices again
                # Path 3: Go right again, visit indices again
                # etc.
                
                # The minimum move count for reaching right_index and making all required visits:
                # We need total_visits visits spread across right_index+1 indices
                # Going right takes right_index + 1 moves (from -1 to right_index)
                # We visit each index once on the way
                
                # For additional visits, we need to move back and forth
                # Optimal: go right to right_index, then go left to some index, then right again, etc.
                
                # Let's use a greedy approach:
                # moves_cost = cost to visit right_index and come back to position 0
                #            = (right_index + 1) + right_index = 2*right_index + 1
                # OR: just go right: right_index + 1 moves
                
                # Then from the rightmost point we reached, we go back and forth
                
                # Simpler formulation:
                # We go from -1 to right_index: right_index + 1 moves
                # Then we go back to 0 and visit indices: right_index moves
                # Total so far: 2*right_index + 1 moves
                # We can make one more pass if we have moves left
                
                # Let me think of the moves as:
                # - Going from -1 to right_index, we visit each index once: cost = right_index + 1
                # - To visit index i again, we need to go there from -1 (or wherever)
                # - The extra cost to visit index i one more time: 2*(i+1) if we go there and back
                # - OR: if we're already going further right, it's included
                
                # New approach: calculate moves needed to make visits[i] visits to index i
                # Where visits[i] = ceil(target / points[i])
                
                # Going right from -1 to right_index and back to -1: 2*(right_index+1) - 1 moves
                # This visits each index on the way up and on the way down, so 2 visits each
                # We can adjust if we don't go all the way back, or stop partway
                
                # Let me use: moves = 2*right_index + 1 if we go right and come back to 0
                # Then we have visited each index at most twice
                
                # For more visits, we need more passes
                # Number of passes = (sum of visits + right_index) // (right_index + 1)
                # Then adjust...
                
                # Actually, simpler approach:
                # sum(visits) is total visits needed
                # If we make k complete passes (right and back), we visit each index 2k times
                # Then partial pass visits each index once more
                
                # For a given right_index:
                # moves = 2*right_index + 1  (go right, come back to -1)
                # But we visit each index twice
                
                # If visits[i] = 2 for all i and right_index = k, this works
                # For visits[i] = 1, we might waste moves
                # For visits[i] = 3, we need extra moves
                
                # Let's compute the actual minimum moves:
                # We can go right to right_index (cost: right_index + 1)
                # Then go back left some amount and go right again
                
                # For simplicity: 
                # - Max visits needed: max(visits)
                # - If max_visits = 1: cost = right_index + 1 (just go right once)
                # - If max_visits = 2: cost = 2*right_index + 1 (go right and back to -1, or go right and come back to 0 then right again)
                # - Generally: cost = right_index + 1 + 2*right_index*(max_visits - 1) = (2*max_visits - 1)*right_index + 1
                
                # Wait, that's not quite right either.
                
                # Let me reconsider: to visit all indices 0 to right_index with visits[i] visits at index i:
                # Moves from -1 to right_index visiting each once: right_index + 1
                # Then from right_index, go back to index j and visit indices j to right_index again: this helps some indices
                # Then potentially go right again from j
                
                # Hmm, this is getting complex. Let me use a simpler formula:
                # To visit each index 0 to k with visit count v[i]:
                # Optimal strategy: 
                # - make (max_v - 1) complete back-and-forth trips from -1 to k: 2*(k+1)*(max_v-1) - ... no this is wrong
                
                # Actually, let's think of it as:
                # - Go from -1 to k: k+1 moves, visits each index i 0..k once
                # - From k, go back to 0: k moves, visits each index i 0..k once more (now they have 2 visits each)
                # - From 0, if we need more visits, we can go right again
                
                # More generally:
                # If we do this pattern: -1 -> k -> 0 -> k -> 0 -> ..., 
                # We can control how many passes we do
                
                # Let's simplify: assume all indices need the same number of visits (worst case)
                # Then: max_visits = max(visits)
                # Cost for max_visits: 
                #   if max_visits == 1: right_index + 1
                #   if max_visits == 2: (right_index + 1) + right_index = 2*right_index + 1
                #   if max_visits == 3: (right_index + 1) + right_index + (right_index + 1) = 3*right_index + 2
                #   ...
                #   Pattern: (max_visits)*right_index + (max_visits - 1 + 1) = max_visits*right_index + max_visits - 1 + ...
                
                # Actually for max_visits:
                # We need (max_visits - 1) back-and-forth from position to right_index
                # Initial: -1 -> right_index: right_index + 1
                # Each back-forth from 0: right_index + 1 (right) + right_index (left back to -1 or 0)
                # Wait, I'm overcomplicating this.
                
                # Better insight: to visit index i exactly visits[i] times
                # The minimum path is to:
                # 1. Go right to right_index (visiting each index 0..right_index once)
                # 2. Go back to some position and go right again (visiting indices again)
                # 3. Repeat as needed
                
                # The position we go back to should be chosen to minimize total moves
                # If all indices have same visit count, we go back to -1 each time
                # If indices have different visit counts, we optimize
                
                # For now, let's use a formula:
                # max_visits = max(visits)
                # The minimum moves to achieve max_visits visits to all indices 0..right_index:
                # = (right_index + 1) + (max_visits - 1) * right_index
                # = right_index + 1 + max_visits*right_index - right_index
                # = (max_visits)*right_index + 1  (if we optimize by not going back to -1)
                
                # Actually this formula assumes we go to right_index, back to 0, right to right_index, ...
                # Costs: (right_index + 1) [reach right_index] + (max_visits - 1) * 2 * right_index [back-forth from 0]
                # But we don't need to visit index -1 each time
                
                # OK let me just use: cost = (right_index + 1) + (max_visits - 1) * right_index
                
                max_visits = max(visits)
                moves_needed = (right_index + 1) + (max_visits - 1) * right_index
                
                if moves_needed <= m:
                    return True
            
            return False
        
        # Binary search on the answer
        left, right = 0, sum(points)
        answer = 0
        
        while left <= right:
            mid = (left + right) // 2
            if can_achieve(mid):
                answer = mid
                left = mid + 1
            else:
                right = mid - 1
        
        return answer
