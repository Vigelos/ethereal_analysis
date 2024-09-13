import pandas as pd
import argparse
import os

def find_pattern_indices(code, pattern):
# find the indices of a pattern in the code
    indices = []
    start = 0
    while True:
        index = code.find(pattern, start)
        if index == -1:  # Pattern not found
            break
        indices.append(index)
        start = index + len(pattern)  # Move past the last found occurrence
    return indices

def inspect_code(code):
# check if the code is a Groth16 implementation
# Three conditions:
# 
#   1. contains SNARK primes
#      NB: Currently this is not required,
#          uncomment line 36 and 37 to enable this check
# 
#   2. contains Pairing check
# 
#   3. preapre space for 24 uint256 variables
#      -A, B, alpha, beta, vk_x, gamma, C delta
# 

    # 0. check if the code is not empty
    if pd.isna(code):
        return False
    
    # 1. check if the code contains SNARK primes
    if "30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47" not in code:
        return False
    # if "30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f0000001" not in code:
    #     return False
    
    # 2. check if the code contains Pairing check
    if "60086107d05a03fa" not in code:
        return False
    
    # 3. check if the code contains preparing space for 24 uint256 variables
    indices = find_pattern_indices(code, "60086107d05a03fa")
    if indices != []:
        for index in indices:
            if "610300" in code[index-64:index]:
                return True
    
    return False

def main():
    # read csv file
    path = "output/contract.csv"
    df = pd.read_csv(path)
    bytecode = df["bytecode"][0]
    
    # check if the code is a Groth16 implementation
    if inspect_code(bytecode):
        is_groth16 = True
    else:
        is_groth16 = False

    # save this new column to the csv file
    df["is_groth16"] = is_groth16
    df.to_csv(path, index=False)

if __name__ == "__main__":
    main()