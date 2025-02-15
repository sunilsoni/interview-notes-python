"""
**Problem:**

Your task is to implement a simulation of a `change directory` command. This command changes the current working directory to the specified one.

- The initial working directory is root i.e. `/`.
- You are given a list of `cd` commands.

There are multiple options for command arguments:

- `cd /` - changes the working directory to the root directory.
- `cd .` - stays in the current directory.
- `cd ..` - moves the working directory one level up. In the root directory, `cd ..` does nothing.
- `cd <subdirectory>` - moves to the specified subdirectory within the current working directory. `<subdirectory>` is a string consisting of only lowercase English letters.

All specified directories exist. Return the absolute path from the root to the working directory after executing all `cd` commands in the given order. `/` should be used as separators.

**Note:** You are not expected to provide the most optimal solution, but a solution with time complexity not worse than `O(commands.length^2 × max(commands[i].length))` will fit within the execution time limit.

---

**Example:**

1. For `commands = ["cd users", "cd codesignal", "cd ..", "cd admin"]`, the output should be `solution(commands) = "/users/admin"`.

    - **Explanation:**
      - The absolute path is changing in the following way:
        `/` -> `/users` -> `/users/codesignal` -> `/users` -> `/users/admin`.

2. For `commands = ["cd users", "cd .", "cd admin", "cd /", "cd volumes"]`, the output should be `solution(commands) = "/volumes"`.

    - **Explanation:**
      - The absolute path is changing in the following way:
        `/` -> `/users` -> `/users` -> `/users/admin` -> `/` -> `/volumes`.

---

**Input/Output:**

- **[execution time limit]** 4 seconds (py3)
- **[memory limit]** 1 GB
- **[input]** array of strings `commands`: An array of strings representing the list of `cd` commands.
    - Guaranteed constraints: `1 ≤ commands.length ≤ 1000`.
- **[output]** string: The current working directory after executing all `cd` commands.

---

**Solution Template:**

```python
def solution(commands):
    # Your code here
```
"""


def solution(commands):
    """
    Simulates a sequence of cd commands to determine the final working directory.

    Args:
    commands (list of str): List of cd commands.

    Returns:
    str: The absolute path of the final working directory.
    """
    # Use a list as a stack to track the current directory path
    path_stack = []

    for command in commands:
        # Remove the "cd " prefix from the command
        argument = command[3:].strip()  # commands always start with "cd "

        if argument == "/":
            # Reset to root directory
            path_stack = []
        elif argument == ".":
            # Stay in the same directory; do nothing
            continue
        elif argument == "..":
            # Move one directory up, if not already at root
            if path_stack:
                path_stack.pop()
        else:
            # Move to the specified subdirectory
            path_stack.append(argument)

    # Build the absolute path from the stack.
    # If the stack is empty, we are at the root.
    return "/" if not path_stack else "/" + "/".join(path_stack)


if __name__ == "__main__":
    # List of test cases as dictionaries with 'commands' and 'expected' keys.
    tests = [
        {
            "commands": ["cd users", "cd codesignal", "cd ..", "cd admin"],
            "expected": "/users/admin"
        },
        {
            "commands": ["cd users", "cd .", "cd admin", "cd /", "cd volumes"],
            "expected": "/volumes"
        },
        {
            "commands": ["cd /", "cd users", "cd projects", "cd ..", "cd .."],
            "expected": "/"
        },
        {
            "commands": ["cd users", "cd ..", "cd ..", "cd admin"],
            "expected": "/admin"
        },
        {
            "commands": ["cd .", "cd .", "cd ."],
            "expected": "/"
        },
        {
            "commands": ["cd a", "cd b", "cd c", "cd ..", "cd d"],
            "expected": "/a/b/d"
        }
    ]

    # Testing each test case.
    all_passed = True
    for idx, test in enumerate(tests):
        result = solution(test["commands"])
        if result == test["expected"]:
            print(f"Test case {idx + 1} PASS: Commands: {test['commands']} => Output: {result}")
        else:
            print(
                f"Test case {idx + 1} FAIL: Commands: {test['commands']} => Output: {result}, Expected: {test['expected']}")
            all_passed = False

    # Testing with large data input to ensure performance.
    # Create a sequence of 1000 commands that alternate between going to a subdirectory and moving up.
    large_commands = []
    # First, go deep into directories
    for i in range(500):
        large_commands.append(f"cd dir{i}")
    # Then, move up 250 levels
    for i in range(250):
        large_commands.append("cd ..")
    # Finally, go to a new subdirectory
    large_commands.append("cd newdir")

    # Expected: The final path should be root plus the remaining directories (500 - 250) directories then /newdir.
    expected_large = "/" + "/".join([f"dir{i}" for i in range(500 - 250)]) + "/newdir"
    large_result = solution(large_commands)
    if large_result == expected_large:
        print(f"Large Input Test PASS: Output: {large_result}")
    else:
        print(f"Large Input Test FAIL: Output: {large_result}, Expected: {expected_large}")
        all_passed = False

    if all_passed:
        print("All test cases passed!")
    else:
        print("Some test cases failed.")
