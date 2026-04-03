def getMaximumThroughput(throughput, scalingCost, budget):
    l, r = 0, 10**18
    ans = 0
    n = len(throughput)

    while l <= r:
        mid = (l + r) // 2
        cost = 0
        ok = True

        for i in range(n):
            if throughput[i] >= mid:
                continue
            need = (mid + throughput[i] - 1) // throughput[i] - 1
            cost += need * scalingCost[i]
            if cost > budget:
                ok = False
                break

        if ok:
            ans = mid
            l = mid + 1
        else:
            r = mid - 1

    return ans


def run_tests():
    tests = [
        ([7,3,4,6],[2,5,4,3],25,9),
        ([3,2,5],[2,5,10],28,6),
        ([4,2,7],[3,5,6],32,10),
    ]

    for i,(t,c,b,exp) in enumerate(tests):
        res = getMaximumThroughput(t,c,b)
        print("Test",i+1,"PASS" if res==exp else "FAIL","->",res)

    import random
    n = 100000
    t = [random.randint(1,100) for _ in range(n)]
    c = [random.randint(1,50) for _ in range(n)]
    b = 10**9
    print("Large Test Output:",getMaximumThroughput(t,c,b))


if __name__ == "__main__":
    run_tests()