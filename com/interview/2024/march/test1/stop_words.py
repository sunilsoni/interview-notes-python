from collections import Counter


def stop_words1(text, k):
    # Split the text into words
    words = text.split()
    # Count the occurrences of each word
    word_counts = Counter(words)
    # Find the words that occur at least k times
    common_words = [word for word, count in word_counts.items() if count >= k]
    # Maintain the order of words as they appear in the text
    ordered_common_words = []
    for word in words:
        if word in common_words and word not in ordered_common_words:
            ordered_common_words.append(word)
    return ordered_common_words


def stop_words(text, k):
    # Split the text into words
    words = text.split()

    # Initialize a dictionary to store word counts
    word_counts = {}

    # Iterate through the words and count occurrences
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    # Initialize a list to store stop words
    stop_words_list = []

    # Iterate through the word counts and add stop words to the list
    for word in words:
        if word_counts[word] >= k and word not in stop_words_list:
            stop_words_list.append(word)

    return stop_words_list


# Example usage
text = "a mouse is smaller than a dog but a dog is stronger"
k = 2
print(stop_words(text, k))

# Example usage:
print(stop_words('text_example', 2))
