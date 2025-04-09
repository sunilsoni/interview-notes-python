def funcFizzBuzz(inputNum):
    """
    Returns the FizzBuzz result for a single integer.
    - "FizzBuzz" if inputNum is multiple of both 3 and 5
    - "Fizz" if multiple of 3 only
    - "Buzz" if multiple of 5 only
    - Otherwise, the number itself as a string
    """
    if inputNum % 15 == 0:  # multiple of both 3 and 5
        return "FizzBuzz"
    elif inputNum % 3 == 0:
        return "Fizz"
    elif inputNum % 5 == 0:
        return "Buzz"
    else:
        return str(inputNum)

def main():
    """
    1) Reads an integer N from standard input.
    2) Prints out the FizzBuzz results for all i in [1..N].
    """
    # Read the integer from user input
    N = int(input().strip())

    # For each number from 1 to N, compute and print the FizzBuzz result
    for i in range(1, N + 1):
        result = funcFizzBuzz(i)
        print(result)

if __name__ == "__main__":
    main()
