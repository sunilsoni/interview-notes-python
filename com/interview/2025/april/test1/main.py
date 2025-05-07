def main(input):
    data = input.strip().split()
    t = int(data[0])
    idx = 1
    results = []

    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = list(map(int, data[idx:idx + n]))
        idx += n
        b = list(map(int, data[idx:idx + n]))
        idx += n

        diff = [a[i] - b[i] for i in range(n)]

        if sum(diff) != 0:
            results.append(-1)
            continue

        positive = sum(d for d in diff if d > 0)
        results.append(positive)

    for res in results:
        print(res)


import sys

s = sys.stdin.read()
main(s)
