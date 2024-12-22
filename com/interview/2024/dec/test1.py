from collections import defaultdict
import re


class ReviewAnalyzer:
    def __init__(self):
        self.word_counts = defaultdict(int)
        self.ngram_counts = defaultdict(int)

    def split_into_sentences(self, review):
        """
        Splits a review into sentences based on ., !, ? delimiters.
        """
        # Use regex to split on punctuation followed by space or end of string
        sentences = re.split(r'[.!?]+', review)
        # Remove any leading/trailing whitespace and filter out empty strings
        return [sentence.strip() for sentence in sentences if sentence.strip()]

    def tokenize(self, sentence):
        """
        Tokenizes a sentence into words, converting to lowercase and removing non-alphanumeric characters.
        """
        # Use regex to find words, ignoring punctuation
        return re.findall(r'\b\w+\b', sentence.lower())

    def count_ngrams(self, tokens, n=1):
        """
        Counts n-grams in a list of tokens.
        """
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i + n])
            self.ngram_counts[ngram] += 1
            if n == 1:
                self.word_counts[ngram] += 1

    def process_reviews(self, reviews, n=1):
        """
        Processes a list of reviews to count n-grams.
        """
        for review in reviews:
            sentences = self.split_into_sentences(review)
            for sentence in sentences:
                tokens = self.tokenize(sentence)
                if tokens:
                    self.count_ngrams(tokens, n)

    def get_word_counts(self):
        """
        Returns the word counts as a sorted list of tuples.
        """
        return sorted(self.word_counts.items(), key=lambda item: item[1], reverse=True)

    def get_ngram_counts(self):
        """
        Returns the n-gram counts as a sorted list of tuples.
        """
        return sorted(self.ngram_counts.items(), key=lambda item: item[1], reverse=True)

    def reset_counts(self):
        """
        Resets the counts.
        """
        self.word_counts = defaultdict(int)
        self.ngram_counts = defaultdict(int)

    def run_tests(self):
        """
        Runs predefined test cases and outputs pass/fail.
        """
        test_cases = [
            {
                'input': [
                    "I loved it! Great space movie.",
                    "A movie about space invasion!",
                    "Best space movie ever!",
                ],
                'n': 1,
                'expected': {
                    'i': 1, 'loved': 1, 'it': 1, 'great': 1, 'space': 3, 'movie': 3,
                    'a': 1, 'about': 1, 'invasion': 1, 'best': 1, 'ever': 1
                }
            },
            {
                'input': [
                    "I loved it! Great space movie.",
                    "A movie about space invasion!",
                    "Best space movie ever!",
                ],
                'n': 2,
                'expected': {
                    'i loved': 1, 'loved it': 1, 'great space': 1, 'space movie': 2,
                    'a movie': 1, 'movie about': 1, 'about space': 1, 'space invasion': 1,
                    'best space': 1, 'space movie': 2, 'movie ever': 1
                }
            },
            {
                'input': [
                    "",
                    "!!!",
                    "Hello.",
                    "Hello world! Hello.",
                ],
                'n': 1,
                'expected': {
                    'hello': 2, 'world': 1
                }
            },
            {
                'input': [
                    "Test",
                    "Test test",
                    "Test-test test."
                ],
                'n': 1,
                'expected': {
                    'test': 4
                }
            }
        ]

        for idx, case in enumerate(test_cases, 1):
            self.reset_counts()
            self.process_reviews(case['input'], case['n'])
            if case['n'] == 1:
                result = dict(self.word_counts)
            else:
                result = dict(self.ngram_counts)
            expected = case['expected']
            if result == expected:
                print(f"Test Case {idx}: PASS")
            else:
                print(f"Test Case {idx}: FAIL")
                print(f"Expected: {expected}")
                print(f"Got: {result}")

        # Large data test case
        self.reset_counts()
        large_reviews = ["space movie " * 10000]  # 10,000 repetitions
        self.process_reviews(large_reviews, n=1)
        expected_large = {'space': 10000, 'movie': 10000}
        result_large = dict(self.word_counts)
        if result_large == expected_large:
            print("Large Data Test Case: PASS")
        else:
            print("Large Data Test Case: FAIL")
            print(f"Expected: {expected_large}")
            print(f"Got: {result_large}")


def main():
    analyzer = ReviewAnalyzer()
    analyzer.run_tests()


if __name__ == "__main__":
    main()
