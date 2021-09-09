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
    def getSignature(self,shingles, rand_hashes):
        result = []
        for (a,b) in self.rand_hashes:
            result.append(self.minHashing(shingles, a, b))
        return result
    
    def forward(self, corpus:List[str]) -> List[int]:
        Sig_Mat = []
        for text in tqdm(corpus):
            shingles = self.getShingles(text, n_shingles=self.n_shingles)
            Sig_Mat.append(self.getSignature(shingles, self.rand_hashes))
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

# 최적의 b,r 찾기 -> 틀린 것임.
_integration_precision = 0.001
def _integration(f, a, b):
    p = _integration_precision
    area = 0.0
    x = a
    while x < b:
        area += f(x+0.5*p)*p
        x += p
    return area, None

try:
    from scipy.integrate import quad as integrate
except ImportError:
    # For when no scipy installed
    integrate = _integration


def _false_positive_probability(threshold, b, r):
    _probability = lambda s : 1 - (1 - s**float(r))**float(b)
    a, err = integrate(_probability, 0.0, threshold)
    return a


def _false_negative_probability(threshold, b, r):
    _probability = lambda s : 1 - (1 - (1 - s**float(r))**float(b))
    a, err = integrate(_probability, threshold, 1.0)
    return a


def _optimal_param(threshold, num_perm, false_positive_weight,
        false_negative_weight):
    '''
    Compute the optimal `MinHashLSH` parameter that minimizes the weighted sum
    of probabilities of false positive and false negative.
    '''
    min_error = float("inf")
    opt = (0, 0)
    for b in range(1, num_perm+1):
        max_r = int(num_perm / b)
        for r in range(1, max_r+1):
            fp = _false_positive_probability(threshold, b, r)
            fn = _false_negative_probability(threshold, b, r)
            error = fp*false_positive_weight + fn*false_negative_weight
            if error < min_error:
                min_error = error
                opt = (b, r)
    return opt

