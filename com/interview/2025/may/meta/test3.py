from typing import List
from dataclasses import dataclass

@dataclass
class Workshop:
    name: str
    classes_per_year: int
    start: int
    end: int


def largest_number_of_classes(workshops: List[Workshop]) -> int:
    # Initialize a dictionary to hold the total classes each year
    classes_by_year = {}

    # Process each workshop to record total classes per year
    for workshop in workshops:
        for year in range(workshop.start, workshop.end + 1):
            # Add the classes per year to the total for that year
            classes_by_year[year] = classes_by_year.get(year, 0) + workshop.classes_per_year

    # Sort the years to ensure consecutive checking
    sorted_years = sorted(classes_by_year.keys())

    # Find the maximum number of classes over two actual consecutive years (no gaps)
    max_classes = 0
    for i in range(len(sorted_years) - 1):
        if sorted_years[i + 1] == sorted_years[i] + 1:
            consecutive_sum = classes_by_year[sorted_years[i]] + classes_by_year[sorted_years[i + 1]]
            max_classes = max(max_classes, consecutive_sum)

    # Handle single-year edge cases if no consecutive years found
    if max_classes == 0 and classes_by_year:
        max_classes = max(classes_by_year.values())

    return max_classes


# Simple main test method without unit tests
def main():
    # Provided test cases
    input_1 = [
        Workshop(name="Intro to archival science", classes_per_year=4, start=2000, end=2003),
        Workshop(name="Bind your own book", classes_per_year=1, start=2001, end=2004),
        Workshop(name="Monthly discussion circle", classes_per_year=12, start=2004, end=2006),
    ]
    assert largest_number_of_classes(input_1) == 25

    input_2 = [
        Workshop(name="Birdwatching for everyone", classes_per_year=13, start=2001, end=2010),
        Workshop(name="Cover restoration", classes_per_year=4, start=2016, end=2020),
        Workshop(name="Make paper from scratch!", classes_per_year=2, start=2019, end=2020),
        Workshop(name="Weekly guest lecture", classes_per_year=52, start=2014, end=2018),
        Workshop(name="Talk like a pirate day", classes_per_year=1, start=2015, end=2015),
    ]
    assert largest_number_of_classes(input_2) == 112

    input_3 = [
        Workshop(name="Volunteer bazaar", classes_per_year=18, start=2011, end=2015),
        Workshop(name="Founder's lecture", classes_per_year=17, start=2017, end=2020),
        Workshop(name="Weekly guest lecture", classes_per_year=52, start=2022, end=2022),
    ]
    assert largest_number_of_classes(input_3) == 36

    input_4 = []  # Edge case with no workshops
    assert largest_number_of_classes(input_4) == 0

    input_5 = [
        Workshop(name="Single year event", classes_per_year=10, start=2020, end=2020)
    ]
    assert largest_number_of_classes(input_5) == 10

    # Additional large-scale test for performance verification
    large_input = [Workshop(name=f"Workshop {i}", classes_per_year=i % 5 + 1, start=2000 + (i % 10), end=2020) for i in range(1000)]
    result = largest_number_of_classes(large_input)
    print(f"Result for large input test: {result}")
    assert result > 0  # Basic assertion to confirm it computes without error

    print("All tests passed.")


if __name__ == "__main__":
    main()
