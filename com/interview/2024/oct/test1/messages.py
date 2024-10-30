import unittest
import re
from collections import defaultdict
import random
import string

"""
Imagine there is a group chat with many users writing messages. The content of messages includes text and mentions of other users in the chat. Mentions in the group chat are formatted as strings starting with @ character and followed by at least one id separated by commas. An id is formatted as a string starting with id and followed by a positive integer from 1 to 999 .
For example:
• "This is an ex@mple with no mentions@"
• "This is an example with @idi one mention of one user"
• "This is an example with @id1,id123,id983 one mention of three users"
• "This is an example with @id1,id123,id983 several mentions of several users @id239"
Now, imagine you are given two arrays of strings titled members and messages. Your task is to calculate the mention statistics for the group chat. In other words, count the number of messages that each chat member is mentioned in. Chat members mentioned multiple times in a message should be counted only once per message.
Return the mention statistics in an array of strings, where each string follows this format: "[user id]=[mentions count]". The array should be sorted by mention count in descending order, or in case of a tie, lexicographically by user id in ascending order.
It is guaranteed that proper ids will be used for each mention. Additionally, all mentions will be preceded by and followed by a space, unless they are located at either the beginning or end of the message. Note that the @ character is still allowed to be included in a message not as a part of any mention, but not as the first character in a word
Note: You are not expected to provide the most optimal solution, but a solution with time complexity not worse than (members. length * messages. length * max(messages [i]. length)) will fit within the execution time limit.
Example
For members = ["id123", "id234", "id7", "id321"] | and
messages = [
"Hey @id123,id321 review this PR please! @id123 what do you think about this approach?",
"Hey @id7 nice appro@ch! Great job! @id800 what do you think?",
"@id123,id321 thx!"
the output should be solution(members, messages) = ["id123=2", "id321=2", "id7=1", "id234=0"].
Explanation:
• In the first message, 2 users are mentioned: id123 and id321. Note that id123 is mentioned twice in this message, but it should only be counted once.

Explanation:
• In the first message, 2 users are mentioned: id123 and id321. Note that id123 is mentioned twice in this message, but it should only be counted once.
• In the second message, 2 users are mentioned: id7 and id800. Note that id800 is not a member of the group chat and that approach and doa are not mentions at all.
• In the third message, 2 users are mentioned: id123 and id321.
• Since "id123" is lexicographically less than "id321"
), the output should be ["id123=2", "id321=2", "id7=1", "id234=0"] -
Input/Output
• [execution time limit] 4 seconds (py3)
• [memory limit] 1 GB
• [input] array.string members
An array of strings representing members of a group chat.
Guaranteed constraints:
2 ≤ members. length ≤ 50,
3 ≤ members[i].length ≤ 5 .
• [input] array.string messages
An array of strings containing messages with text and user mentions described above.
Guaranteed constraints:
1 ≤ messages. length ≤ 100 ,
1 ≤ messages [i]. length ≤ 1000 .
• [output] array.string
An array of strings containing all user ids from members , with mention statistics of each user id across
messages (described above) separated by = sign. This array should be sorted by
mention count in descending order, or in case of a tie, lexicographically by user id in ascending order.

Provide test method to check if PASS/FAIL all test cases also handle large data inputs cases

def solution (members, messages) :"""

def solution(members, messages):
    mention_count = defaultdict(int)

    for message in messages:
        mentioned = set()
        mentions = re.findall(r'@((?:id\d+,?)+)', message)
        for mention in mentions:
            for user_id in mention.split(','):
                if user_id in members:
                    mentioned.add(user_id)
        for user_id in mentioned:
            mention_count[user_id] += 1

    for member in members:
        if member not in mention_count:
            mention_count[member] = 0

    result = [f"{user_id}={count}" for user_id, count in mention_count.items()]
    return sorted(result, key=lambda x: (-int(x.split('=')[1]), x.split('=')[0]))


class TestSolution(unittest.TestCase):
    def test_example_case(self):
        members = ["id123", "id234", "id7", "id321"]
        messages = [
            "Hey @id123,id321 review this PR please! @id123 what do you think about this approach?",
            "Hey @id7 nice appro@ch! Great job! @id800 what do you think?",
            "@id123,id321 thx!"
        ]
        expected = ["id123=2", "id321=2", "id7=1", "id234=0"]
        self.assertEqual(solution(members, messages), expected)

    def test_no_mentions(self):
        members = ["id1", "id2", "id3"]
        messages = ["Hello world", "No mentions here", "Just plain text"]
        expected = ["id1=0", "id2=0", "id3=0"]
        self.assertEqual(solution(members, messages), expected)

    def test_all_mentioned(self):
        members = ["id1", "id2", "id3"]
        messages = ["@id1,id2,id3 Hello everyone!"]
        expected = ["id1=1", "id2=1", "id3=1"]
        self.assertEqual(solution(members, messages), expected)

    def test_multiple_mentions_same_message(self):
        members = ["id1", "id2"]
        messages = ["@id1 @id1 @id2 @id1 @id2"]
        expected = ["id1=1", "id2=1"]
        self.assertEqual(solution(members, messages), expected)

    def test_lexicographic_ordering(self):
        members = ["id2", "id1", "id3"]
        messages = ["@id1,id2,id3", "@id1,id2,id3"]
        expected = ["id1=2", "id2=2", "id3=2"]
        self.assertEqual(solution(members, messages), expected)

    def test_large_input(self):
        def generate_id():
            return 'id' + ''.join(random.choices(string.digits, k=random.randint(1, 3)))

        members = [generate_id() for _ in range(50)]
        messages = []
        for _ in range(100):
            mention_count = random.randint(0, 10)
            mentions = '@' + ','.join(random.choices(members, k=mention_count)) if mention_count > 0 else ''
            message = f"{mentions} {''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 990)))}"
            messages.append(message)

        result = solution(members, messages)

        # Check if all members are in the result
        self.assertEqual(len(result), len(members))

        # Check if the result is correctly sorted
        for i in range(len(result) - 1):
            count1 = int(result[i].split('=')[1])
            count2 = int(result[i + 1].split('=')[1])
            id1 = result[i].split('=')[0]
            id2 = result[i + 1].split('=')[0]
            self.assertTrue(count1 > count2 or (count1 == count2 and id1 < id2))


if __name__ == '__main__':
    unittest.main()
