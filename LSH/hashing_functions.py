import random
from typing import List, Set

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

class MinHashing(object):
    def __init__(self, num_perm, n_shingles, tokenizer):
        self.num_perm = num_perm
        self.rand_hashes = [[random.randint(0, 10 ** 9), random.randint(0, 10 ** 9)] for i in range(num_perm)]
        self.n_shingles = n_shingles
        self.tokenizer = tokenizer
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
    def getShingles(self, text:str) -> List:
        tokenized_text = tokenizer(text)
        result = []
        for i in range(len(text)-self.n_shingles):
            t = tokenized_text[i:i+n_shingles]
            if t:
                result.append(' '.join(t))
        
        return list(set(result))
    # with out speed up
    def minHashing(self, shingles, a, b):
        result = -1
        for shingle in shingles:
            sh = self.stringHashing(shingle)
            h = self.polynomialHashing(sh,a,b)
            if result==-1:
                result = h
            else:
                if result>h:
                    result = h
        return result
    def getSignature(self,shingles):
        result = []
        for (a,b) in self.rand_hashes:
            result.append(self.minHashing(shingles, a, b))
        return result
    
    def forward(self, corpus:List[str]) -> List[int]:
        Sig_Mat = []
        for text in tqdm(corpus):
            shingles = self.getShingles(text)
            Sig_Mat.append(self.getSignature(shingles))
        return Sig_Mat
    def LSH(self, sig_mat, b, r):
        result = []
        for t in range(len(sig_mat)):
            sig = sig_mat[t]
            # band 별로 bucket을 따로 만듬.
            buckets = dict()
            for i in range(b):
                # 세로로 비교 하는 것을 인지해라.
                band = ''.join([str(sig[j]) for j in range(i * r, (i + 1) * r)]) # 이거 자체가 hashing 함수 
                if buckets.get(band, -1)==-1:
                    buckets[band]=set()
                buckets[band].add(t)
            x = list([list(i) for i in buckets.values() if len(list(i))>1])
            result.append(x)
        return result

def getShingles(tokenized_text:List[str], n_shingles:int) -> List:
    result = [tokenized_text[i:i+n_shingles] for i in range(len(text)-n_shingles)]
    return list(set(result))

