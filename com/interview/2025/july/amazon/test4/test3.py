from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


# Abstract base class for file criteria
class FileCriteriaStrategy(ABC):
    @abstractmethod
    def matches(self, file_path: Path) -> bool:
        """Abstract method that all criteria strategies must implement"""
        pass


# Concrete strategies for different criteria types
class SizeCriteria(FileCriteriaStrategy):
    def __init__(self, size_mb: float):
        self.size_threshold = size_mb

    def matches(self, file_path: Path) -> bool:
        return file_path.stat().st_size / (1024 * 1024) > self.size_threshold


class ExtensionCriteria(FileCriteriaStrategy):
    def __init__(self, extension: str):
        self.extension = extension.lower()

    def matches(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == self.extension


class NameContainsCriteria(FileCriteriaStrategy):
    def __init__(self, pattern: str):
        self.pattern = pattern.lower()

    def matches(self, file_path: Path) -> bool:
        return self.pattern in file_path.name.lower()


# Composite criteria for combining multiple criteria
class AndCriteria(FileCriteriaStrategy):
    def __init__(self, *criteria: FileCriteriaStrategy):
        self.criteria = criteria

    def matches(self, file_path: Path) -> bool:
        return all(criterion.matches(file_path) for criterion in self.criteria)


class OrCriteria(FileCriteriaStrategy):
    def __init__(self, *criteria: FileCriteriaStrategy):
        self.criteria = criteria

    def matches(self, file_path: Path) -> bool:
        return any(criterion.matches(file_path) for criterion in self.criteria)


# File search function
def search_files(directory_path: str, criteria: FileCriteriaStrategy) -> List[str]:
    """
    Search for files in a directory based on provided criteria strategy
    """
    dir_path = Path(directory_path)
    matching_files = []

    try:
        for item in dir_path.iterdir():
            if item.is_file() and criteria.matches(item):
                matching_files.append(str(item))
        return matching_files
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


# Usage example
def main():
    test_dir = "test_directory"

    # Test Case 1: Find large files (> 5MB)
    size_criteria = SizeCriteria(5)
    result1 = search_files(test_dir, size_criteria)
    print("\nLarge files:", result1)

    # Test Case 2: Find XML files
    xml_criteria = ExtensionCriteria('.xml')
    result2 = search_files(test_dir, xml_criteria)
    print("\nXML files:", result2)

    # Test Case 3: Find large TXT files (combining criteria)
    large_txt_criteria = AndCriteria(
        SizeCriteria(5),
        ExtensionCriteria('.txt')
    )
    result3 = search_files(test_dir, large_txt_criteria)
    print("\nLarge TXT files:", result3)

    # Test Case 4: Find files containing 'test' OR with .xml extension
    test_or_xml_criteria = OrCriteria(
        NameContainsCriteria('test'),
        ExtensionCriteria('.xml')
    )
    result4 = search_files(test_dir, test_or_xml_criteria)
    print("\nFiles containing 'test' or XML files:", result4)


if __name__ == "__main__":
    main()
