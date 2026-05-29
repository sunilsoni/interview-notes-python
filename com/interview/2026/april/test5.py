def analyze_large_file(file_path):
    # We keep our running trackers outside the loop
    total_word_count = 0
    longest_word = ""

    # Open the file in read mode ('r').
    # Using 'with' ensures the file closes automatically when we are done.
    with open(file_path, 'r', encoding='utf-8') as file:

        # This loop reads the file ONE line at a time.
        # It never loads the whole file into memory.
        for line in file:

            # Split only the current line into words
            words_in_line = line.split()

            # Add this line's word count to our running total
            total_word_count += len(words_in_line)

            # Check for the longest word just in this specific line
            for word in words_in_line:
                if len(word) > len(longest_word):
                    longest_word = word

    # Return the final tallies after reading the very last line
    return (total_word_count, longest_word)