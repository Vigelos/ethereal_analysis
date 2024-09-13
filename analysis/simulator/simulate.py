from vulnerability_detectors import *
from util import *
import pandas as pd

def detect_vulnerabilities(bytecode, debug=False):

    instructions = disassemble(bytecode=bytecode)
    
    snark_scalar_field_detector = SnarkScalarFieldDetector(instructions,debug=False)
    prime_q_detector = PrimeQFieldDetector(instructions,debug=False)

    entry_point_idx_snark_field = snark_scalar_field_detector.get_entry_point_idx()
    entry_point_idx_prime_q = prime_q_detector.get_entry_point_idx()

    if debug:
        print("check snark field from entry point idx: ", entry_point_idx_snark_field)
    have_snark_scalar_field, have_prime_q = False, False
    for idx in entry_point_idx_snark_field:
        try:
            snark_scalar_field_detector.run(idx)
        except Exception as e:
            if "SNARK Scalar Field constraint detected" in str(e):
                have_snark_scalar_field = True
    if debug:
        print("check prime q from entry point idx: ", entry_point_idx_prime_q)

    for idx in entry_point_idx_prime_q:
        try:
            prime_q_detector.run(idx)
        except Exception as e:
            if "Prime Q constraint detected" in str(e):
                have_prime_q = True
            else:
                raise e
    
    return have_snark_scalar_field, have_prime_q

def main():
    # read the bytecode from the csv file
    df = pd.read_csv("output/contract.csv")
    bytecode = df["bytecode"][0]
    simulator_has_R, simulator_has_Q = detect_vulnerabilities(bytecode)
    df["simulator_has_R"] = simulator_has_R
    df["simulator_has_Q"] = simulator_has_Q
    df.to_csv("output/contract.csv", index=False)

if __name__ == "__main__":
    main()
    # df = pd.read_csv("../Groth16Contracts.csv")
    # simulator_have_snark_scalar_field = []
    # simulator_have_prime_q = []
    # for i in range(len(df)):
    #     bytecode = df.loc[i, "code"]
    #     print("checking contract: {}".format(df.loc[i, "contract_address"]) )
    #     have_snark_scalar_field, have_prime_q = detect_vulnerabilities(bytecode)
    #     simulator_have_prime_q.append(have_prime_q)
    #     simulator_have_snark_scalar_field.append(have_snark_scalar_field)
    
    # # save to info csv
    # info = pd.read_csv("../Groth16Contracts_info.csv")
    # info["simulator_have_snark_scalar_field"] = simulator_have_snark_scalar_field
    # info["simulator_have_prime_q"] = simulator_have_prime_q

    # info.to_csv("../Groth16Contracts_info.csv", mode='w', header=True, index=False)
