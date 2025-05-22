from typing import Dict, List, Optional
from collections import Counter

def most_common_comment(comments: Dict[str, List[str]]) -> Optional[str]:
    if not comments:
        return None

    # Count all unique comments per location
    counter = Counter()
    for location_comments in comments.values():
        unique_comments = set(location_comments)  # Remove duplicates within location
        counter.update(unique_comments)           # Count each unique comment only once per shop

    if not counter:
        return None

    # Return comment with highest count
    return max(counter.items(), key=lambda x: x[1])[0]
def main():
    input_1 = {
        "Blue Hill": ["Cozy atmosphere", "Curated selection", "Too busy"],
        "Apple Road": ["Good parking", "Sweets are delicious", "Perfect for rainy days"],
        "Orange Avenue": ["Large bike storage", "Curated selection"],
    }
    assert most_common_comment(input_1) == "Curated selection"

    input_2 = {
        "Olive Street": ["Lively atmosphere", "Cozy atmosphere", "Too busy"],
        "Green Gardens": ["Good lighting", "Lively atmosphere", "Rustic feel"],
        "Cherry Hill": ["Vibrant atmosphere", "Vibrant atmosphere", "No parking"],
        "Apple Road": ["Cozy interior", "Vibrant atmosphere", "Vibrant atmosphere"],
        "Orange Avenue": ["Too noisy", "Lively atmosphere"],
    }
    assert most_common_comment(input_2) == "Lively atmosphere"

    input_3 = {
        "Green Gardens": ["Cozy atmosphere", "Cozy atmosphere"],
        "Blue Road": ["Rustic feel"],
    }
    assert most_common_comment(input_3) in ["Cozy atmosphere", "Rustic feel"]

    input_4 = {
        "Green Gardens": ["Cozy atmosphere", "Cozy atmosphere"],
        "Blue Road": ["Rustic feel"],
        "Apple Road": ["Rustic feel", "No parking"],
        "Cherry Hill": ["Rustic feel", "Good lighting"]
    }
    assert most_common_comment(input_4) == "Rustic feel"

    input_5 = {}
    assert most_common_comment(input_5) == None

    print("All tests passed.")

main()
