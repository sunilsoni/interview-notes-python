#!/usr/bin/env python3
"""
Python 3.x
Problem:
  Simulate how a simple word processor (e.g. Google Docs) would wrap
  English (and other Unicode) text into lines of a fixed page width.
  We do not split words across lines. We honor explicit newline characters
  by forcing a break. Tabs are treated as single spaces for simplicity.
"""

def count_lines(text, width):
    """
    Count how many lines 'text' will occupy on a page of character-width 'width'.
    - We assume each character (including Unicode) counts as length 1.
    - Explicit '\\n' in the text forces a new line.
    - '\\t' is converted to a space.
    """

    # 1) Normalize tabs: treat each tab as a single space character.
    #    In a real word processor tabs might be variable width,
    #    but for simplicity we map them to one space.
    text = text.replace('\t', ' ')

    # 2) Split on explicit newlines so we handle each paragraph separately.
    #    Each '\n' forces the end of the current line, even if it's empty.
    paragraphs = text.split('\n')

    total_lines = 0      # Accumulate lines across all paragraphs

    # Process each paragraph (the text between two '\n')
    for para in paragraphs:

        # If the paragraph is empty (i.e. two consecutive '\n'),
        # that still occupies exactly one blank line.
        if para == "":
            total_lines += 1
            # Move on to the next paragraph
            continue

        # Split the paragraph into words on spaces.
        # Multiple spaces collapse into multiple empty tokens,
        # so we filter them out with split().
        words = para.split()

        # Start each new paragraph on line 1
        line_count = 1
        # current_len tracks how many characters are on the current line so far
        current_len = 0

        # Fit each word greedily onto the current line if possible
        for word in words:
            w = len(word)            # length of this word in characters

            if current_len == 0:
                # Case A: The line is empty — put the word here directly
                # No leading space is needed.
                current_len = w
            elif current_len + 1 + w <= width:
                # Case B: The word (plus a leading space) fits:
                #   current_len + 1 (for the space) + w (word length)
                current_len += 1 + w
            else:
                # Case C: It does NOT fit — wrap to a new line:
                line_count += 1
                # Place the word at the start of the new line
                current_len = w

        # Add this paragraph’s line count to the total
        total_lines += line_count

    return total_lines


def main():
    """
    A simple main() to exercise count_lines() without any testing framework.
    Prints PASS/FAIL for each scenario, including a large-data check.
    """

    test_cases = [
        # (input_text, page_width, expected_line_count)
        ("", 80, 0),  # empty document → zero lines
        ("Hello", 5, 1),  # one word fits exactly on one line
        ("Hello world", 5, 2),  # second word ("world") wraps
        ("The quick brown fox jumps over the lazy dog", 10, 5),
        ("a b\tc\n\nd e", 3, 5),
        # Explanation for above:
        #  "a" on line1,
        #  "b c" on line2 (tab→space),
        #  blank line3 (empty paragraph),
        #  "d e" wraps into 2 lines? Actually width=3 → "d" on line4, "e" on line5.
        ("longword", 4, 1),  # longword > width but occupies one line
        ("word " * 100000, 10, None),  # large data: just check it returns an int
    ]

    for idx, (text, width, expected) in enumerate(test_cases, start=1):
        result = count_lines(text, width)

        if expected is None:
            # For large-data we only assert we got an integer back
            status = "PASS" if isinstance(result, int) else "FAIL"
        else:
            status = "PASS" if result == expected else f"FAIL (got {result})"

        print(f"Test {idx:2d}: width={width:3d} → lines={result:6} : {status}")


if __name__ == "__main__":
    main()