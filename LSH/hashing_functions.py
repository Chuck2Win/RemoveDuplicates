# polynomial rolling hash function
# s : string
# s[0]+s[1]*p + s[2]*(p**2) + .. + s[n-1]*(p**(n-1))
def stringHashing(text:str)->int:
    result = 0
    p = 53 # character의 개수만큼
    m = 10**9 + 7 # 충분히 크게 
    for i in range(len(text)):
        result += (ord(text[i])*(p**i))
    return result % m
# polynomial hashing
# 1차 함수 통과시키고 p(충분히 큰수)로 나눠줌.
def polynomialHashing(x,a,b):
  p = 10**9+7
  return (a*x+b)%p

import random

class MinHashing(object):
    def __init__(self, num_perm, n_shingles):
        self.num_perm = num_perm
        self.rand_hashes = [[random.randint(0, 10 ** 9), random.randint(0, 10 ** 9)] for i in range(num_perm)]
        self.n_shingles = n_shingles
    def stringHashing(self, text:str)->int:
        result = 0
        p = 53 # character의 개수만큼
        m = 10**9 + 7 # 충분히 크게 
        for i in range(len(text)):
            result += (ord(text[i])*(p**i))
        return result % m
    def polynomialHashing(self, x:int, a:int, b:int) -> int:
        p = 10 ** 9 + 7
        return (a * x + b) % p
    # shingles 만들기
    def getShingles(self, text:str, n_shingles:int) -> List:
        result = [text[i:i+n_shingles] for i in range(len(text)-n_shingles)]
        return list(set(result))
    
    def minHashing(self, shingles, a, b):
        result = -1
        for shingle in shingles:
            sh = stringHashing(shingle)
            h = polynomialHashing(sh,a,b)
            if result==-1:
                result = h
            else:
                if result>h:
                    result = h
        return result
    def getSignature(self,shingles, rand_hashes):
        result = []
        for (a,b) in self.rand_hashes:
            result.append(self.minHashing(shingles, a, b))
        return result
    def forward(self, text:str) -> List[int]:
        shingles = self.getShingles(text, n_shingles=self.n_shingles)
        return self.getSignature(shingles, self.rand_hashes)
