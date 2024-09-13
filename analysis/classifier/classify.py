import pandas as pd
from Prototype import *

def main():   
    # read bytecode from contract.csv
    df = pd.read_csv("output/contract.csv")
    bytecode = df["bytecode"][0]
    predict_has_R_constraint = df["predict_has_R_constraint"][0]
    predict_has_Q_constraint = df["predict_has_Q_constraint"][0]

    contract = Contract(bytecode, predict_has_R_constraint, predict_has_Q_constraint)

    # save to csv
    df["bytecode_fingerprint"] = contract.finger_print
    df["prototype_name"] = contract.prototype
    df["prototype_info"] = contract.info
    df["prototype_address"] = contract.address
    df.to_csv("output/contract.csv", index=False)
        
if __name__ == "__main__":
    main()