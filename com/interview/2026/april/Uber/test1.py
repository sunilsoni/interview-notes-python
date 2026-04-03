def finalPrice(prices):
    n=len(prices)
    res=prices[:]
    st=[]
    for i,p in enumerate(prices):
        while st and prices[st[-1]]>=p:
            j=st.pop()
            res[j]=prices[j]-p
        st.append(i)
    total=sum(res)
    full=[i for i in st]
    return total,full

def run_test(inp,exp_sum,exp_idx):
    s,idx=finalPrice(inp)
    ok=(s==exp_sum and idx==exp_idx)
    print("PASS" if ok else "FAIL",inp,"->",s,idx)

if __name__=="__main__":
    run_test([1,3,3,2,5],9,[0,3,4])
    run_test([5,1,3,4,6,2],14,[1,5])
    run_test([2,3,1,2,4,2],8,[2,5])
    import random
    big=[random.randint(1,10**6) for _ in range(10**5)]
    finalPrice(big)