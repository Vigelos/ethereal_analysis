import pandas as pd
import re
import os
import argparse

SNARK_SCALAR_FIELD = "0x30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f0000001"
PRIME_Q = "0x30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47"

def check_completeness_of_decompiled_code(decompiled_code,log_level=0):
    if "address(0x08).{ gas: gasleft() - 0x07d0 }staticcall(" not in decompiled_code:
        # print("[Config Warning]: Pairing Check Opcode (0x08) is missing, decompliation may be incorrect")
        return False
    else:
        return True

def check_require_information_heimdall(decompiled_code,log_level=0):

    # select the lines where require( condition, "information") occurs
    def find_require(code_in_line):
        indices = []
        for i, line in enumerate(code_in_line):
            if "require" in line:
                indices.append(i)
        return indices
    
    # extract the condition and information from the require statement
    def extract_require_information(code_in_line, indices, log_level=0):
        conditions = []
        informations = []
        for index in indices:
            line = code_in_line[index]
            condition = line.split("require(")[1].split(",")[0]
            try:
                information = line.split("require(")[1].split(",")[1][:-2]
            except:
                information = ""
            conditions.append(condition)
            informations.append(information)
            if log_level>0:
                print("-------------\nRequire Code detected:")
                print("   Condition: ", condition)
                if information:
                    print("   Information: ", information)
        return conditions, informations
    
    if log_level>0:
        print("======================\nChecking require information in the code")

    # break the code into lines
    code_in_line = decompiled_code.split("\n")

    # find the index where the require command is
    require_index = find_require(code_in_line)

    # extract the condition and information from the require statement
    conditions, informations = extract_require_information(code_in_line, require_index, log_level)

    have_snark_scalar_field = False
    have_prime_Q = False

    for condition in conditions:
        if "< 0x30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47" in condition:
            have_prime_Q = True
        if "< 0x30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f0000001" in condition:
            have_snark_scalar_field = True
    
    # if not have_snark_scalar_field:
        # print("[Security Warning]: Input to SNARK_scalar_field constraint is missing (0x30644e...000001)")
        # or input is incorrectly checked against Prime_Q, instead of SNARK_scalar_field
    # 
    # if not have_prime_Q:
    #     print("[Security Warning]: Proof to Prime_Q constraint is missing (0x30644e...7cfd47)")
    
    # if have_snark_scalar_field and have_prime_Q:
    #     print("[Finish]: SNARK_scalar_field and Prime Q constraints are satisfied")

    # print("======================\n")
    return have_snark_scalar_field, have_prime_Q

def decompile_with_heimdall(bytecode):
    # get decompiled code form Heimdall
    command = "/Users/vigelos/.bifrost/bin/heimdall decompile {} --include-sol".format(bytecode)
    os.system(command)
    with open("output/local/decompiled.sol", 'r') as f:
        decompiled_sol_code = f.read()

    return decompiled_sol_code

def decompileCodeAnalysis(bytecode):
    decompiled_code = decompile_with_heimdall(bytecode)
    is_decompile_complete = check_completeness_of_decompiled_code(decompiled_code)
    have_snark_scalar_field, have_prime_Q = check_require_information_heimdall(decompiled_code)
    return is_decompile_complete, have_snark_scalar_field, have_prime_Q


def main():
    # read bytecode from csv file
    df = pd.read_csv("output/contract.csv")
    bytecode = df["bytecode"][0]
    is_decompile_complete, have_snark_scalar_field, have_prime_Q = decompileCodeAnalysis(bytecode)

    # save the new column to the csv file
    df["is_decompile_complete"] = is_decompile_complete
    df["decompile_has_R"] = have_snark_scalar_field
    df["decompile_has_Q"] = have_prime_Q
    df.to_csv("output/contract.csv", index=False)

if __name__ == "__main__":
    main()