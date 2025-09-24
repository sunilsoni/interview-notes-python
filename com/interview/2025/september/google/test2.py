#!/usr/bin/env python3
"""
Python 3.x
Enhanced word‐processor–style wrapper with hyphenation:
  • Honors explicit newlines as paragraph breaks.
  • Normalizes any '\r\n', '\r' → '\n'.
  • Treats '\t' as a single space.
  • Never splits words unless they exceed the line width—in which
    case they’re hyphenated (e.g. 'jumped' → 'jump‐' + 'ed').
  • Returns the fully wrapped lines, so you can both inspect
    hyphenation and count the lines.
"""

def wrap_text(text, width):
    """
    Wrap `text` onto lines of at most `width` characters,
    inserting hyphens for overlong words.
    Returns:
      List[str]: each element is one line (with trailing hyphens if needed).
    """

    # 0) Empty‐document shortcut
    if text == "":
        return []

    # 1) Normalize newline variants → '\n'
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # 2) Simplify tabs to single spaces
    text = text.replace('\t', ' ')

    # 3) Split into paragraphs on '\n'
    paras = text.split('\n')
    wrapped_lines = []

    # 4) Process each paragraph separately
    for para in paras:
        if para == "":
            # Explicit blank line → preserve it
            wrapped_lines.append("")
            continue

        words = para.split()  # split on whitespace; keeps punctuation attached
        current = ""           # build up the current line here

        for word in words:
            wlen = len(word)

            # A) If the word itself is longer than width → hyphenate
            if wlen > width:
                #  A1) flush any existing text on the current line
                if current:
                    wrapped_lines.append(current)
                    current = ""

                #  A2) break the overlong word into width‐1 chunks + hyphen
                remainder = word
                while len(remainder) > width:
                    # take first (width-1) chars, add '-'
                    part = remainder[:width-1]
                    wrapped_lines.append(part + "-")
                    remainder = remainder[width-1:]
                # the leftover 'remainder' now fits on one line
                current = remainder

            else:
                # B) word fits by itself in an empty line?
                if not current:
                    current = word
                # C) word fits after a space?
                elif len(current) + 1 + wlen <= width:
                    current = current + " " + word
                else:
                    # D) needs wrap → flush current, start new line
                    wrapped_lines.append(current)
                    current = word

        # 5) End of paragraph → flush any last line
        wrapped_lines.append(current)

    return wrapped_lines


def count_lines(text, width):
    """
    Simply returns how many lines wrap_text() produces.
    """
    return len(wrap_text(text, width))


def main():
    # Demonstration on the classic pangram + hyphenation example
    text = "The quick brown fox jumped over the lazy dog."
    width = 5
    lines = wrap_text(text, width)

    print(f"Wrapping to width={width}:")
    for i, line in enumerate(lines, start=1):
        print(f"{i:2d}: '{line}'")
    print(f"\nTotal lines: {count_lines(text, width)}")


if __name__ == "__main__":
    main()