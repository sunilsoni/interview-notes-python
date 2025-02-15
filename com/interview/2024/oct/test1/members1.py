import re


def solution(members, messages):
    """
    Calculates the mention statistics for each member in the group chat.

    :param members: A list of strings representing member IDs.
    :param messages: A list of messages containing text and mentions.
    :return: A list of strings in the format "[user id]=[mentions count]" sorted as specified.
    """
    member_set = set(members)
    mention_counts = {member: 0 for member in members}

    # Regular expression pattern to match mentions
    pattern = r'(?<!\S)@((?:id[1-9]\d{0,2})(?:,id[1-9]\d{0,2})*)'

    for message in messages:
        # Find all mentions in the message
        matches = re.finditer(pattern, message)
        mentions_in_message = set()
        for match in matches:
            ids_str = match.group(1)
            ids = ids_str.split(',')
            mentions_in_message.update(ids)
        # Count valid mentions
        valid_mentions = mentions_in_message.intersection(member_set)
        for member in valid_mentions:
            mention_counts[member] += 1

    # Sort the members by mention count (descending), then by user id (ascending)
    sorted_members = sorted(
        mention_counts.items(),
        key=lambda x: (-x[1], x[0])
    )

    # Format the output
    result = [f"{member}={count}" for member, count in sorted_members]
    return result


def run_tests():
    """
    Runs a series of test cases to verify the correctness of the solution function.
    Outputs 'PASS' if the test case passes, and 'FAIL' along with details if it fails.
    """
    test_cases = [
        # Test case 1: Example from the problem description
        (
            ["id123", "id234", "id7", "id321"],
            [
                "Hey @id123,id321 review this PR please! @id123 what do you think about this approach?",
                "Hey @id7 nice appro@ch! Great job! @id800 what do you think?",
                "@id123,id321 thx!"
            ],
            ["id123=2", "id321=2", "id7=1", "id234=0"]
        ),
        # Test case 2: No mentions
        (
            ["id1", "id2"],
            ["Hello world!", "No mentions here."],
            ["id1=0", "id2=0"]
        ),
        # Test case 3: Multiple mentions in one message
        (
            ["id1", "id2", "id3"],
            ["@id1,id2,id3,id1,id2"],
            ["id1=1", "id2=1", "id3=1"]
        ),
        # Test case 4: Mentions of non-members
        (
            ["id1", "id2"],
            ["@id3,id4 Hello!", "@id1,id2 Hi!"],
            ["id1=1", "id2=1"]
        ),
        # Test case 5: Members not mentioned
        (
            ["id100", "id200", "id300"],
            ["@id100 Hi!", "@id200 Hello!", "@id100 How are you?"],
            ["id100=2", "id200=1", "id300=0"]
        ),
        # Test case 6: Edge case with maximum id number
        (
            ["id999", "id1"],
            ["@id999,@id1 Check this out.", "@id999 What do you think?"],
            ["id999=2", "id1=1"]
        ),
        # Test case 7: Large data input
        (
            [f"id{i}" for i in range(1, 51)],
            [f"Message {j} @id{j % 50 + 1},@id{(j + 1) % 50 + 1}" for j in range(1, 101)],
            None  # We'll compute the expected output in the test
        ),
        # Test case 8: Mentions at the start and end of messages
        (
            ["id1", "id2", "id3"],
            ["@id1,id2 Hello there!", "This is a message for @id2,id3", "Goodbye @id1,id3"],
            ["id1=2", "id2=2", "id3=2"]
        ),
        # Test case 9: Mentions with special characters nearby
        (
            ["id1", "id2"],
            ["Check this out@id1,id2!", "Wait@id1,id2, there's more."],
            ["id1=0", "id2=0"]
        ),
        # Test case 10: Mentions with numbers in text
        (
            ["id10", "id20"],
            ["Hey @id10,id20, check id100 and id200.", "@id10 id20 is not mentioned properly."],
            ["id10=2", "id20=1"]
        ),
    ]

    all_passed = True

    for idx, (members, messages, expected_output) in enumerate(test_cases):
        output = solution(members, messages)

        # For test case 7, compute the expected output
        if expected_output is None:
            mention_counts = {f"id{i}": 0 for i in range(1, 51)}
            for j in range(1, 101):
                mention_counts[f"id{j % 50 + 1}"] += 1
                mention_counts[f"id{(j + 1) % 50 + 1}"] += 1
            sorted_members = sorted(
                mention_counts.items(),
                key=lambda x: (-x[1], x[0])
            )
            expected_output = [f"{member}={count}" for member, count in sorted_members if member in members]

        if output == expected_output:
            print(f"Test case {idx + 1}: PASS")
        else:
            all_passed = False
            print(f"Test case {idx + 1}: FAIL")
            print(f"  Members: {members}")
            print(f"  Messages: {messages}")
            print(f"  Expected output: {expected_output}")
            print(f"  Actual output:   {output}")

    if all_passed:
        print("\nAll test cases passed!")
    else:
        print("\nSome test cases failed.")


if __name__ == "__main__":
    run_tests()
