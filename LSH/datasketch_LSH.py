from datasketch import MinHash, MinHashLSH
import xxhash
from typing import List,Dict,Tuple,Set
import os
import re
from tqdm import tqdm

data_dir = r'./preprocessed_data'
n_shingle = 5
num_perm = 128
bands = 32
rows = 4 
threshold = 0.9
# 순서 shingle화 -> min hashing -> LSH 로 유사도 계산.

def minHash(seq:List[str], num_perm=num_perm):
    m = MinHash(num_perm = num_perm, hashfunc=xxhash.xxh64_intdigest)
    for s in seq:
        m.update(s.encode('utf-8'))
    return LeanMinHash(m)

# tokenized 된 text를 활용해야함.
def getShingles(tokenized_text:List[str], n_shingle:int):
    x = set()
    for i in range(len(tokenized_text)-n_shingle):
        temp = tokenized_text[i:i+n_shingle]
        s = ''
        for i in temp:
            s+=' '+i
        x.add(s.strip())
    return x
    
def lsh_similar(minhashes, bands, rows, threshold):
    Result = {}
    lsh = MinHashLSH(num_perm=num_perm, params=(bands, rows), threshold=threshold)
    for i, mh in enumerate(tqdm(minhashes)):
        lsh.insert(i, mh)
    for i,mh in enumerate(tqdm(minhashes)):
        result = lsh.query(mh)
        Result[i]=result
    return Result
