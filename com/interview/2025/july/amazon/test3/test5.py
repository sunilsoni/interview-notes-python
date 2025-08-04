from enum import Enum
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union


class SizeComparison(Enum):
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    EQUAL = "=="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    NOT_EQUAL = "!="


class SizeUnit(Enum):
    BYTES = 1
    KB = 1024
    MB = 1024 * 1024
    GB = 1024 * 1024 * 1024


class SizeCriteria(FileCriteriaStrategy):
    def __init__(self,
                 size: float,
                 comparison: SizeComparison,
                 unit: SizeUnit = SizeUnit.MB):
        self.size = size
        self.comparison = comparison
        self.unit = unit
        self._comparison_ops = {
            SizeComparison.LESS_THAN: lambda x, y: x < y,
            SizeComparison.LESS_THAN_OR_EQUAL: lambda x, y: x <= y,
            SizeComparison.EQUAL: lambda x, y: abs(x - y) < 0.001,  # Using small delta for float comparison
            SizeComparison.GREATER_THAN: lambda x, y: x > y,
            SizeComparison.GREATER_THAN_OR_EQUAL: lambda x, y: x >= y,
            SizeComparison.NOT_EQUAL: lambda x, y: abs(x - y) >= 0.001,
        }

    def _get_size_in_units(self, file_path: Path) -> float:
        """Convert file size to specified unit"""
        return file_path.stat().st_size / self.unit.value

    def matches(self, file_path: Path) -> bool:
        file_size = self._get_size_in_units(file_path)
        compare_func = self._comparison_ops[self.comparison]
        return compare_func(file_size, self.size)


# Helper factory class for more readable criteria creation
class FileSizeCriteria:
    @staticmethod
    def larger_than(size: float, unit: SizeUnit = SizeUnit.MB) -> SizeCriteria:
        return SizeCriteria(size, SizeComparison.GREATER_THAN, unit)

    @staticmethod
    def smaller_than(size: float, unit: SizeUnit = SizeUnit.MB) -> SizeCriteria:
        return SizeCriteria(size, SizeComparison.LESS_THAN, unit)

    @staticmethod
    def equals(size: float, unit: SizeUnit = SizeUnit.MB) -> SizeCriteria:
        return SizeCriteria(size, SizeComparison.EQUAL, unit)

    @staticmethod
    def between(min_size: float, max_size: float,
                unit: SizeUnit = SizeUnit.MB) -> 'AndCriteria':
        return AndCriteria(
            SizeCriteria(min_size, SizeComparison.GREATER_THAN_OR_EQUAL, unit),
            SizeCriteria(max_size, SizeComparison.LESS_THAN_OR_EQUAL, unit)
        )


# Usage examples
def main():
    test_dir = "test_directory"

    # Example 1: Files exactly 1MB
    exact_size = SizeCriteria(1, SizeComparison.EQUAL, SizeUnit.MB)

    # Example 2: Files larger than 500KB
    larger_than_500kb = SizeCriteria(500, SizeComparison.GREATER_THAN, SizeUnit.KB)

    # Example 3: Files between 1MB and 10MB
    between_1_and_10mb = FileSizeCriteria.between(1, 10, SizeUnit.MB)

    # Example 4: Files smaller than 1GB
    smaller_than_1gb = FileSizeCriteria.smaller_than(1, SizeUnit.GB)

    # Example 5: Combining size criteria with other criteria
    large_txt_files = AndCriteria(
        FileSizeCriteria.larger_than(5, SizeUnit.MB),
        ExtensionCriteria('.txt')
    )

    # Example 6: Complex size criteria
    complex_size = OrCriteria(
        FileSizeCriteria.smaller_than(100, SizeUnit.KB),
        FileSizeCriteria.larger_than(1, SizeUnit.GB)
    )

    # Running searches
    results = {
        "Exactly 1MB": search_files(test_dir, exact_size),
        "Larger than 500KB": search_files(test_dir, larger_than_500kb),
        "Between 1MB and 10MB": search_files(test_dir, between_1_and_10mb),
        "Smaller than 1GB": search_files(test_dir, smaller_than_1gb),
        "Large TXT files": search_files(test_dir, large_txt_files),
        "Very small or very large": search_files(test_dir, complex_size)
    }

    # Print results
    for description, files in results.items():
        print(f"\n{description}:")
        for file in files:
            print(f"  - {file}")


if __name__ == "__main__":
    main()
