import random
import string
import unittest

"""
You are given a string text consisting of unique lowercase English words that are divided by spaces.
Your task is to count the absolute difference between the number of vowels (which are 'a' , 'e' | 'i'
"'o'
, and 'u' ) and the number of consonants in each word. You
are to return the array of words in the ascending order of these absolute differences. If the absolute difference is the same, sort the words in alphabetical order.
Note: You are not expected to provide the most optimal solution, but a solution with time complexity not worse than o(text. length?) will fit within the execution time limit.
Example
• Example 1: For text = "penelope lives in hawaii"
, the output should be solution(text) = ["in", "penelope", "lives", "hawaii"]
Explanation:
Step 1:
*Word "penelope" contains 4 consonants (p, n, 1 and p) and 4 vowels (e, e, o and e ). Since 4 - 4 = 0, the absolute difference is 0 .
*Word "lives" contains 3 consonants (1, v and s) and 2 vowels (i and e ). Since 3 - 2 = 1, the absolute difference is 1.
*Word "in" contains 1 consonant (n) and 1 vowel (i ). Since 1 - 1 = 0, the absolute difference is 0.
*Word "hawaii" contains 2 consonants (h and w) and 4 vowels (a, a, i and i). Since 2 - 4 = -2, the absolute difference is 2 .
Step 2:
Since 0 = 0 < 1 < 2, the words can be sorted in the ascending order with the exception where both "penelope" and
"in" have absolute difference of 0. In this
case, the words are sorted in alphabetical order (i.e., "in" goes before "penelope" ).
Therefore, the answer is ['"in", "penelope", "lives", "hawaii"].
• Example 2: For text = "aabb cepp aaap a"
, the output should be solution (text) = ["aabb", "a", "aaap", "ccpp"] .
Explanation:

Explanation:
Step 1:
*Word "aabb" contains 2 consonants (b and b) and 2 vowels ( a, a ). Since 2 - 2 = 0, the absolute difference is 0 .
*Word "cepp" contains 4 consonants (c, c p and p) and 0 vowels. Since 4 - 0 = 4, the absolute difference is 4.
* Word "aaap" contains 1 consonant (p) and 3 vowels. Since 1 - 3 = -2, the absolute difference is 2.
*Word "a" contains 0 consonants and 1 vowel. Since 0 - 1 = -1, the absolute difference is 1.
Step 2:
Since 0 < 1 < 2 < 4, the answer is ["aabb", "a", "aaap", "ссрр"] .
Input/Output
• [execution time limit] 4 seconds (py3)
• [memory limit] 1 GB
• [input] string text
A string of unique words divided by spaces. Words will include only lowercase English letters. The maximum length of the words in the text is 20 characters.
Guaranteed constraints:
1 ≤ text.length ≤ 1000 .
• [output] array.string
Return the array of strings in the ascending order of the absolute difference between the count of vowels (aeiou) and consonants in each word in text .

def solution(text):"""


class Solution:
    def solution(self, text):
        words = text.split()
        vowels = set('aeiou')

        def count_difference(word):
            vowel_count = sum(1 for char in word if char in vowels)
            consonant_count = len(word) - vowel_count
            return abs(vowel_count - consonant_count)

        return sorted(words, key=lambda w: (count_difference(w), w))


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        text = "penelope lives in hawaii"
        expected = ["in", "penelope", "lives", "hawaii"]
        self.assertEqual(self.sol.solution(text), expected)

    def test_example_2(self):
        text = "aabb ccpp aaap a"
        expected = ["aabb", "a", "aaap", "ccpp"]
        self.assertEqual(self.sol.solution(text), expected)

    def test_all_vowels(self):
        text = "aaa eee iii ooo uuu"
        expected = ["aaa", "eee", "iii", "ooo", "uuu"]
        self.assertEqual(self.sol.solution(text), expected)

    def test_all_consonants(self):
        text = "bcd fgh jkl mnp qrs tvw xyz"
        expected = ["bcd", "fgh", "jkl", "mnp", "qrs", "tvw", "xyz"]
        self.assertEqual(self.sol.solution(text), expected)

    def test_mixed_case(self):
        text = "ab bc cd de ef fg"
        expected = ["ab", "bc", "cd", "de", "ef", "fg"]
        self.assertEqual(self.sol.solution(text), expected)

    def test_large_input(self):
        def generate_word():
            length = random.randint(1, 20)
            return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

        words = [generate_word() for _ in range(1000)]
        text = ' '.join(words)
        result = self.sol.solution(text)

        self.assertEqual(len(result), 1000)
        self.assertEqual(set(result), set(words))

        # Check if the result is correctly sorted
        vowels = set('aeiou')

        def count_difference(word):
            vowel_count = sum(1 for char in word if char in vowels)
            consonant_count = len(word) - vowel_count
            return abs(vowel_count - consonant_count)

        for i in range(len(result) - 1):
            diff1 = count_difference(result[i])
            diff2 = count_difference(result[i + 1])
            self.assertTrue(diff1 <= diff2 or (diff1 == diff2 and result[i] <= result[i + 1]))

    def test_edge_cases(self):
        self.assertEqual(self.sol.solution("a"), ["a"])
        self.assertEqual(self.sol.solution("z"), ["z"])
        self.assertEqual(self.sol.solution("aa zz"), ["aa", "zz"])


if __name__ == '__main__':
    unittest.main()
