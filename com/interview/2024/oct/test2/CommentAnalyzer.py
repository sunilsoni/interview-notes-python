import time
from collections import Counter
from typing import Optional, Dict, List

"""from typing import Dict, List, Optional
The bookstore gathered a list of customer comments from each shop location, and wants to find the most common comment across all locations (ignoring duplicates from the same location).• If multiple comments appear the same number of times, return-any one of them.
Example: f
"Blue Hill": ["Cozy atmosphere", "Curated-selection", "Too-busy"],
"Apple Road": • •
- ["Good-parking", "Sweets are delicious", "Perfect for rainy days"],
"Orange Avenue": • ["Large bike-storage", "Curated selection"],
Result: "Curated selection"
def most_common_comment (comments: Dict[str, List[str]]) -> Optional[str] :
• #- Code here
return. ""
#• Tests
input_1 = f
"Blue Hill":
• ["Cozy atmosphere", "Curated-selection", "Too busy"],
"Apple Road": ["Good parking", "Sweets are delicious", "Perfect for rainy days"],
"Orange Avenue": • ["Large bike storage"
, "Curated selection" ],
assert (most_common_comment (input_1) == "Curated selection" )
input_2 = f
"Olive Street": • ["Lively atmosphere", "Cozy atmosphere", "Too-busy"],
"Green Gardens": ["Good-lighting", "Lively atmosphere", "Rustic feel"],
"Cherry Hill": • ["Vibrant atmosphere", "Vibrant atmosphere", "No parking"],
"Apple Road":.. ["Cozy interior"
, "Vibrant atmosphere", "Vibrant atmosphere"],
"Orange Avenue": ["Too noisy", "Lively atmosphere"],
assert (most_common_comment (input_2) == "Lively atmosphere" )
input_3 = f
"Green Gardens": • ["Cozy atmosphere", "Cozy atmosphere"],
"Blue Road":
["Rustic feel"],
}"""


class CommentAnalyzer:
    @staticmethod
    def most_common_comment(reviews: Dict[str, List[str]]) -> Optional[str]:
        """
        Finds the most frequently occurring comment across all café reviews,
        counting each unique comment only once per location.

        Args:
            reviews: Dictionary with café names as keys and lists of comments as values

        Returns:
            Most common comment or None if no reviews exist
        """
        if not reviews:
            return None

        # Count comments across locations, ignoring duplicates within same location
        comment_counter = Counter()
        for location, comments in reviews.items():
            # Convert to set to remove duplicates within same location
            unique_comments = set(comments)
            comment_counter.update(unique_comments)

        if not comment_counter:
            return None

        # Get the most common comment
        most_common = comment_counter.most_common(1)
        return most_common[0][0] if most_common else None


def run_tests():
    test_cases = [
        {
            "input": {
                "Blue Hill": ["Cozy atmosphere", "Curated selection", "Too busy"],
                "Apple Road": ["Good parking", "Sweets are delicious", "Perfect for rainy days"],
                "Orange Avenue": ["Large bike storage", "Curated selection"]
            },
            "expected": "Curated selection",
            "name": "Test 1: Basic case"
        },
        {
            "input": {
                "Olive Street": ["Lively atmosphere", "Cozy atmosphere", "Too busy"],
                "Green Gardens": ["Good lighting", "Lively atmosphere", "Rustic feel"],
                "Cherry Hill": ["Vibrant atmosphere", "Vibrant atmosphere", "No parking"],
                "Apple Road": ["Cozy interior", "Vibrant atmosphere", "Vibrant atmosphere"],
                "Orange Avenue": ["Too noisy", "Lively atmosphere"]
            },
            "expected": "Lively atmosphere",  # Now correct as duplicates in same location don't count
            "name": "Test 2: Multiple locations"
        },
        {
            "input": {
                "Green Gardens": ["Cozy atmosphere", "Cozy atmosphere"],
                "Blue Road": ["Rustic feel"]
            },
            "expected": "Cozy atmosphere",
            "name": "Test 3: Duplicates in same location"
        },
        {
            "input": {},
            "expected": None,
            "name": "Test 4: Empty input"
        }
    ]

    def print_analysis(input_data: Dict[str, List[str]]) -> None:
        """Helper function to print detailed analysis"""
        print("\nDetailed Analysis:")

        # Show unique comments per location
        print("Comments per location (after removing duplicates):")
        for location, comments in input_data.items():
            unique_comments = set(comments)
            print(f"{location}: {list(unique_comments)}")

        # Show total frequency across locations
        counter = Counter()
        for comments in input_data.values():
            counter.update(set(comments))  # Count each unique comment once per location
        print("\nTotal frequency across locations:")
        for comment, count in counter.most_common():
            print(f"'{comment}': {count} locations")

    analyzer = CommentAnalyzer()
    total_tests = len(test_cases)
    passed_tests = 0

    print("\nRunning tests...")
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        try:
            start_time = time.time()
            result = analyzer.most_common_comment(test["input"])
            execution_time = (time.time() - start_time) * 1000

            if result == test["expected"]:
                status = "✅ PASS"
                passed_tests += 1
            else:
                status = "❌ FAIL"
                print_analysis(test["input"])

            print(f"Expected: {test['expected']}")
            print(f"Got: {result}")
            print(f"Status: {status}")
            print(f"Execution time: {execution_time:.2f}ms")

        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")

    # Large scale test
    print("\nRunning large scale test...")
    large_input = {
        f"Café_{i}": ["Common comment"] * (i % 3 + 1) + ["Rare comment"]
        for i in range(1000)
    }
    start_time = time.time()
    result = analyzer.most_common_comment(large_input)
    execution_time = (time.time() - start_time) * 1000
    print(f"Large scale test completed in {execution_time:.2f}ms")
    print(f"Result: {result}")
    passed_tests += 1 if result == "Common comment" else 0

    print(f"\nTest Summary:")
    print(f"Passed: {passed_tests}/{total_tests + 1}")
    print(f"Success Rate: {(passed_tests / (total_tests + 1)) * 100:.1f}%")


if __name__ == "__main__":
    run_tests()
