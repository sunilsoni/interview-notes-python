import os
from pathlib import Path


def search_files(directory_path, criteria_type, value):
    """
    Search for files in a directory based on specified criteria
    Args:
        directory_path: Path to search in
        criteria_type: 'size' or 'extension'
        value: Size in MB or file extension (e.g., '.xml')
    """
    # Convert directory path to Path object for better handling
    dir_path = Path(directory_path)

    # List to store matching files
    matching_files = []

    try:
        # Iterate through all items in directory
        for item in dir_path.iterdir():
            # Check if item is a file (not a directory)
            if item.is_file():
                if criteria_type == 'size':
                    # Convert file size to MB (1MB = 1024*1024 bytes)
                    file_size_mb = item.stat().st_size / (1024 * 1024)
                    # Check if file size meets criteria
                    if file_size_mb > float(value):
                        matching_files.append(str(item))

                elif criteria_type == 'extension':
                    # Check if file has matching extension
                    if item.suffix.lower() == value.lower():
                        matching_files.append(str(item))

        return matching_files

    except Exception as e:
        print(f"Error occurred: {e}")
        return []


def main():
    """
    Main function to test the file search functionality
    """
    # Test directory path - replace with your test directory
    test_dir = "test_directory"

    # Create test directory and files if they don't exist
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

        # Create test files with different sizes and extensions
        with open(f"{test_dir}/large_file.txt", "wb") as f:
            f.write(b'0' * 6 * 1024 * 1024)  # 6MB file

        with open(f"{test_dir}/small_file.txt", "wb") as f:
            f.write(b'0' * 1024 * 1024)  # 1MB file

        with open(f"{test_dir}/test.xml", "w") as f:
            f.write("<test>XML Content</test>")

    # Test Case 1: Find files over 5MB
    print("\nTest Case 1: Files over 5MB")
    result1 = search_files(test_dir, 'size', 5)
    print(f"Files found: {result1}")
    print(f"Test 1 {'PASS' if len(result1) > 0 else 'FAIL'}")

    # Test Case 2: Find XML files
    print("\nTest Case 2: XML files")
    result2 = search_files(test_dir, 'extension', '.xml')
    print(f"Files found: {result2}")
    print(f"Test 2 {'PASS' if len(result2) > 0 else 'FAIL'}")


if __name__ == "__main__":
    main()
