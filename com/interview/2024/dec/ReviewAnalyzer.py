import re
from collections import Counter

"""

Let's see what terms are the most common for a movie.
We would like to analyze Amazon Original movie reviews. It would split each review into sentences and
# It stores the words, and word pairs in a big vocabulary with their respective counts.

reviews = [
    "I loved it! Great space movie.",
    "A movie about space invasion!",
    "Best space movie ever!",
]

# result = [('movie', 3),
#           ('space', 3),
#           ('space movie', 2),
#           ('a', 1),
#           ('about', 1),
#           ('invasion', 1), ...]

# I loved it! Great space movie. -> ["I loved it", "Great space movie"]
# ["I loved it", ....] -> (1-gram) "i", "loved", "it" , (2-gram) "i loved", "loved it"
#
# 1 - Can you implement the tokenizer and the word count?
#
# 2 - How would you extend to 2-grams?
#
# 3 - How would you scale it to n-grams?
"""


class ReviewAnalyzer:
    def __init__(self):
        self.unigram_counts = Counter()
        self.bigram_counts = Counter()
        self.trigram_counts = Counter()

    def tokenize(self, sentence):
        """
        Tokenizes a sentence into lowercase words, removing non-alphanumeric characters.

        Args:
            sentence (str): The sentence to tokenize.

        Returns:
            list of str: The list of tokenized words.
        """
        # Use regex to find all word characters, convert to lowercase
        return re.findall(r'\w+', sentence.lower())

    def split_into_sentences(self, review):
        """
        Splits a review into sentences based on punctuation.

        Args:
            review (str): The review text.

        Returns:
            list of str: The list of sentences.
        """
        # Split on ., !, or ? followed by space or end of string
        sentences = re.split(r'[.!?]+', review)
        # Strip whitespace and remove empty strings
        return [sentence.strip() for sentence in sentences if sentence.strip()]

    def count_ngrams(self, sentences, n=1):
        """
        Counts n-grams from a list of sentences.

        Args:
            sentences (list of str): The list of sentences.
            n (int): The size of the n-gram.

        Returns:
            Counter: A Counter object with n-gram counts.
        """
        ngram_counts = Counter()
        for sentence in sentences:
            words = self.tokenize(sentence)
            for i in range(len(words) - n + 1):
                ngram = ' '.join(words[i:i + n])
                ngram_counts[ngram] += 1
        return ngram_counts

    def process_reviews(self, reviews):
        """
        Processes a list of reviews to count unigrams, bigrams, and trigrams.

        Args:
            reviews (list of str): The list of review texts.
        """
        all_sentences = []
        for review in reviews:
            sentences = self.split_into_sentences(review)
            all_sentences.extend(sentences)

        self.unigram_counts = self.count_ngrams(all_sentences, n=1)
        self.bigram_counts = self.count_ngrams(all_sentences, n=2)
        self.trigram_counts = self.count_ngrams(all_sentences, n=3)

    def run_tests(self):
        """
        Runs predefined test cases and prints PASS/FAIL for each.
        """
        # Define test cases
        test_reviews = [
            "I loved it! Great space movie.",
            "A movie about space invasion!",
            "Best space movie ever!"
        ]

        # Expected counts
        expected_unigrams = {
            'i': 1, 'loved': 1, 'it': 1,
            'great': 1, 'space': 3, 'movie': 3,
            'a': 1, 'about': 1, 'invasion': 1,
            'best': 1, 'ever': 1
        }

        expected_bigrams = {
            'i loved': 1, 'loved it': 1,
            'great space': 1, 'space movie': 2,
            'a movie': 1, 'movie about': 1,
            'about space': 1, 'space invasion': 1,
            'best space': 1, 'movie ever': 1
        }

        # Process test reviews
        self.process_reviews(test_reviews)

        # Test unigrams
        test_pass_unigrams = all(self.unigram_counts.get(k, 0) == v for k, v in expected_unigrams.items())
        print("Unigram counts test:", "PASS" if test_pass_unigrams else "FAIL")

        # Test bigrams
        test_pass_bigrams = all(self.bigram_counts.get(k, 0) == v for k, v in expected_bigrams.items())
        print("Bigram counts test:", "PASS" if test_pass_bigrams else "FAIL")

        # Minimal reproducible example
        # Check if 'movie' appears 3 times
        test_pass_movie = (self.unigram_counts.get('movie', 0) == 3)
        print("Test for 'movie' count:", "PASS" if test_pass_movie else "FAIL")

        # Check if 'space movie' appears 2 times
        test_pass_space_movie = (self.bigram_counts.get('space movie', 0) == 2)
        print("Test for 'space movie' bigram count:", "PASS" if test_pass_space_movie else "FAIL")

        # Edge case: empty input
        empty_counts = self.count_ngrams([], n=1)
        test_pass_empty = (len(empty_counts) == 0)
        print("Test empty input:", "PASS" if test_pass_empty else "FAIL")

        # Large data test
        large_data_reviews = test_reviews * 10000
        large_sentences = []
        for review in large_data_reviews:
            sentences = self.split_into_sentences(review)
            large_sentences.extend(sentences)
        large_unigram_counts = self.count_ngrams(large_sentences, n=1)
        # 'movie' should appear 3 * 10000 = 30000 times
        test_pass_large = (large_unigram_counts.get('movie', 0) == 30000)
        print("Test large data 'movie' count:", "PASS" if test_pass_large else "FAIL")

    def display_common_terms(self, top_n=10):
        """
        Displays the top N most common unigrams and bigrams.

        Args:
            top_n (int): Number of top terms to display.
        """
        print(f"Top {top_n} Unigrams:")
        for word, count in self.unigram_counts.most_common(top_n):
            print(f"  {word}: {count}")

        print(f"\nTop {top_n} Bigrams:")
        for bigram, count in self.bigram_counts.most_common(top_n):
            print(f"  {bigram}: {count}")

    def reset_counts(self):
        """
        Resets all counts.
        """
        self.unigram_counts = Counter()
        self.bigram_counts = Counter()
        self.trigram_counts = Counter()


def main():
    analyzer = ReviewAnalyzer()
    analyzer.run_tests()

    # Example usage
    reviews = [
        "I loved it! Great space movie.",
        "A movie about space invasion!",
        "Best space movie ever!",
    ]

    analyzer.process_reviews(reviews)
    analyzer.display_common_terms()


if __name__ == "__main__":
    main()
