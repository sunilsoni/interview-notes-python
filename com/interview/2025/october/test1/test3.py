from collections import Counter
import random

def solution(matrix):
    n=len(matrix)
    m=len(matrix[0])
    row_freq=[Counter(row) for row in matrix]
    col_freq=[Counter(matrix[r][c] for r in range(n)) for c in range(m)]
    ans=0
    for r in range(n):
        fr=row_freq[r]
        for c in range(m):
            x=matrix[r][c]
            if m==1:
                row_ok=True; row_v=None
            else:
                if fr[x]==m:
                    row_ok=True; row_v=x
                elif len(fr)==2 and fr[x]==1:
                    row_ok=True; row_v=next(k for k in fr if k!=x)
                else:
                    row_ok=False; row_v=None
            fc=col_freq[c]
            if n==1:
                col_ok=True; col_v=None
            else:
                if fc[x]==n:
                    col_ok=True; col_v=x
                elif len(fc)==2 and fc[x]==1:
                    col_ok=True; col_v=next(k for k in fc if k!=x)
                else:
                    col_ok=False; col_v=None
            if row_ok and col_ok:
                if row_v is not None and col_v is not None:
                    if row_v==col_v:
                        ans+=1
                else:
                    ans+=1
    return ans

def brute(matrix):
    n=len(matrix); m=len(matrix[0])
    ans=0
    for r in range(n):
        for c in range(m):
            if m==1:
                row_ok=True; row_v=None
            else:
                row_vals=[matrix[r][j] for j in range(m) if j!=c]
                row_ok=len(set(row_vals))==1
                row_v=row_vals[0] if row_ok else None
            if n==1:
                col_ok=True; col_v=None
            else:
                col_vals=[matrix[i][c] for i in range(n) if i!=r]
                col_ok=len(set(col_vals))==1
                col_v=col_vals[0] if col_ok else None
            if row_ok and col_ok:
                if row_v is not None and col_v is not None:
                    if row_v==col_v:
                        ans+=1
                else:
                    ans+=1
    return ans

if __name__ == "__main__":
    tests = [
        ([[1,1,1,1],[2,3,1,1],[1,1,1,0],[1,4,1,1]], 2),
        ([[1,2],[2,1]], 4),
        ([[2,3]], 2),
        ([[7]], 1),
    ]
    for mat, exp in tests:
        print("PASS" if solution(mat)==exp else "FAIL")
    n=m=50
    big=[[5]*m for _ in range(n)]
    print("Large input test passed:", solution(big)==n*m)
    random.seed(1)
    big2=[[random.randint(0,3) for _ in range(m)] for __ in range(n)]
    print("Large input test passed:", solution(big2)==brute(big2))