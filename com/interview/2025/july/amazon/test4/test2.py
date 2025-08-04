import os
from pathlib import Path
from typing import Callable, List

# Define custom types for better readability
FileCriteria = Callable[[Path], bool]


def size_criteria(size_mb: float) -> FileCriteria:
    """
    Creates a size-based file criteria function
    Args:
        size_mb: Size threshold in MB
    Returns:
        Function that checks if file meets size criteria
    """

    def check_size(file_path: Path) -> bool:
        # Convert file size to MB and compare
        return file_path.stat().st_size / (1024 * 1024) > size_mb

    return check_size


def extension_criteria(extension: str) -> FileCriteria:
    """
    Creates an extension-based file criteria function
    Args:
        extension: File extension to match (e.g., '.xml')
    Returns:
        Function that checks if file matches extension
    """

    def check_extension(file_path: Path) -> bool:
        # Compare file extension (case-insensitive)
        return file_path.suffix.lower() == extension.lower()

    return check_extension


def search_files(directory_path: str, criteria_func: FileCriteria) -> List[str]:
    """
    Search for files in a directory based on provided criteria function
    Args:
        directory_path: Path to search in
        criteria_func: Function that determines if a file matches criteria
    Returns:
        List of matching file paths
    """
    dir_path = Path(directory_path)
    matching_files = []

    try:
        # Check each file in directory against criteria
        for item in dir_path.iterdir():
            if item.is_file() and criteria_func(item):
                matching_files.append(str(item))
        return matching_files
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


def main():
    """
    Main function to test the file search functionality
    """
    # Test directory setup
    test_dir = "test_directory"

    # Create test directory and files if they don't exist
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

        # Create test files
        with open(f"{test_dir}/large_file.txt", "wb") as f:
            f.write(b'0' * 6 * 1024 * 1024)  # 6MB file

        with open(f"{test_dir}/small_file.txt", "wb") as f:
            f.write(b'0' * 1024 * 1024)  # 1MB file

        with open(f"{test_dir}/test.xml", "w") as f:
            f.write("<test>XML Content</test>")

    # Test Case 1: Find files over 5MB
    print("\nTest Case 1: Files over 5MB")
    size_finder = size_criteria(5)  # Create size criteria function
    result1 = search_files(test_dir, size_finder)
    print(f"Files found: {result1}")
    print(f"Test 1 {'PASS' if len(result1) > 0 else 'FAIL'}")

    # Test Case 2: Find XML files
    print("\nTest Case 2: XML files")
    xml_finder = extension_criteria('.xml')  # Create extension criteria function
    result2 = search_files(test_dir, xml_finder)
    print(f"Files found: {result2}")
    print(f"Test 2 {'PASS' if len(result2) > 0 else 'FAIL'}")

    # Example of combining criteria
    def combined_criteria(file_path: Path) -> bool:
        """Custom criteria combining size and extension"""
        is_large = size_criteria(5)(file_path)
        is_txt = extension_criteria('.txt')(file_path)
        return is_large and is_txt

    # Test Case 3: Find large TXT files
    print("\nTest Case 3: Large TXT files")
    result3 = search_files(test_dir, combined_criteria)
    print(f"Files found: {result3}")
    print(f"Test 3 {'PASS' if len(result3) > 0 else 'FAIL'}")


if __name__ == "__main__":
    main()
