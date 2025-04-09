
def main():
    # Provided input method
    xCoordinate_size = int(input())
    xCoordinate = list(map(int, input().split()))

    yCoordinate_size = int(input())
    yCoordinate = list(map(int, input().split()))

    result = funcDrop(xCoordinate, yCoordinate)
    print(result)


if __name__ == "__main__":
    main()

