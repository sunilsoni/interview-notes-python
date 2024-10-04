#!/bin/python3

from itertools import combinations


#
# FC Codelona is trying to assemble a team from a roster of available players. They have a minimum number of players they want to sign, and each player needs to have a skill rating within a certain range. Given a list of players' skill levels with desired upper and lower bounds, determine how many teams can be created from the list.
# Example
# skills = [12, 4, 6, 13, 5, 10]
# minPlayers = 3
# minLevel = 4
# maxLevel = 10
# • The list includes players with skill levels [12, 4, 6, 13, 5, 10].
# • They want to hire at least 3 players with skill levels between 4 and 10, inclusive.
# • Four of the players with the following skill levels { 4, 6, 5, 10} meet the criteria.
# • There are 5 ways to form a team of at least 3 players: 14, 5, 63, 14, 6, 107, 14, 5,103, 15, 6, 10}, and 14, 5, 6, 10}
# • Return 5.
# Function Description
# Complete the function countTeams in the editor below.
# countTeams has the following parameters):
# int skills[n]: an array of integers that represent the skill level per player int minPlayers: the minimum number of team members required int minLevel: the lower limit for skill level, inclusive int-maxLevel: the upper limit for skill level, inclusive
# Return
# int: the total number of teams that can be formed per the criteria
# Constraints
# • 1≤n≤ 20
# • 1 ≤ minPlayers ≤n
# • 1 ≤ minLevel ≤ maxLevel ≤ 1000
# • 1 ≤ skills[i] ≤ 1000
#
#
# • Input Format for Custom Testing
# Input from stdin will be processed as follows and passed to the function.
# The first line contains an integer n, the size of the array skills.
# The next n lines each contain an element skills[i] where 0 ≤ i < n.
# The next line contains an integer, minPlayers, the minimum number of players to be included in the team.
# The next line contains an integer, minLevel, the lower limit of skill level to select The next line contains an integer, maxLevel, the upper limit of skill level to select
# • Sample Case 0
# Sample Input 0
# STDIN
# Function
# 4
# 4
# 8
# 5
# 6
# 1
# 5
# 7
# →
# →
# →
# →
# →
# Sample Output 0
# 3
# skills] size n = 4
# skills = 14, 8, 5, 61
# minPlayers = 1
# minLevel = 5
# maxLevel = 7
# Explanation 0
# • The list includes players with skill levels [4, 8, 5, 6].
# • They want to hire at least 1 player with skill levels between 5 and 7, inclusive.
# • Two of the players with the following skill levels { 5, 6} meet the criteria
# • There are 3 ways to form a team of at least 1 player : {5}, {6}, 45, 6} .
# • Returns 3.
#
# • Sample Case 1
# Sample Input 1
# STDIN
# ーーーーー
# 4
# 4
# 8
# 5
# 6
# 2
# 5
# 7
# ↑↑
# →
# Function
# skills] size n = 4
# skills = 14, 8, 5, 61
# minPlayers = 2
# minLevel = 5
# maxLevel = 7
# Sample Output 1
# 1
# Explanation 1
# • The list includes players with skill levels [4, 8, 5, 6}.
# • They want to hire at least 2 players with skill levels between 5 and 7, inclusive.
# • Two of the players with the following skill levels { 5, 6} meet the criteria
# • There is only one ways to form a team of at least 2 players : 45, 6} .
# • Returns 1
#
# • Sample Case 2
# Sample Input 2
# STDIN
# Function
# 4
# 4
# 8
# 5
# 6
# 2
# 7
# 8
# skills|] size n = 4
# skills = 14, 8, 5, 6]
# →
# minPlayers = 2
# minLevel = 7
# maxLevel = 8
# Sample Output 2
# Explanation 2
# • The list includes players with skill levels [4, 8, 5, 61.
# • They want to hire at least 2 players with skill levels between 7 and 8, inclusive.
# • One of the players with the following skill levels ‹ 8} meet the criteria.
# • There is no way to form a team of at least 2 players.
# • Returns 0.

class TeamCounter:
    def countTeams(self, skills, minPlayers, minLevel, maxLevel):
        # Filter skills within the required range
        valid_skills = [skill for skill in skills if minLevel <= skill <= maxLevel]

        # If we don't have enough players, return 0
        if len(valid_skills) < minPlayers:
            return 0

        total_teams = 0

        # Generate all possible combinations of players from minPlayers to total valid players
        for i in range(minPlayers, len(valid_skills) + 1):
            total_teams += len(list(combinations(valid_skills, i)))

        return total_teams


def main():
    # Test cases
    test_cases = [
        ([12, 4, 6, 13, 5, 10], 3, 4, 10, 5),  # Example case
        ([4, 8, 5, 6], 1, 5, 7, 3),  # Sample case 0
        ([4, 8, 5, 6], 2, 5, 7, 1),  # Sample case 1
        ([4, 8, 5, 6], 2, 7, 8, 0)  # Sample case 2
    ]

    counter = TeamCounter()

    for i, (skills, minPlayers, minLevel, maxLevel, expected) in enumerate(test_cases):
        result = counter.countTeams(skills, minPlayers, minLevel, maxLevel)
        print(f"Test case {i + 1}: {'PASS' if result == expected else 'FAIL'}")
        print(f"Expected: {expected}, Got: {result}\n")


if __name__ == "__main__":
    main()
