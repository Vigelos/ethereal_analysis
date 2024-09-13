import pandas as pd
import argparse
import os

SNARK_SCALAR_FIELD = "30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f0000001"
PRIME_Q = "30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47"


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--bytecode", type=str, default=None, help="the bytecode of the smart contract")
    args = parser.parse_args()

    bytecode = args.bytecode
    if bytecode is None:
        print("Error: bytecode is not provided.")
        print("Usage: python main.py --bytecode <bytecode>")
        return
    
    
    # if bytecode not starts with 0x, add it
    if not bytecode.startswith("0x"):
        bytecode = "0x" + bytecode

    # save the bytecode to a csv file
    df = pd.DataFrame({"bytecode": [bytecode]})
    path = "output/contract.csv"
    df.to_csv(path, index=False)

    # check if the bytecode is a Groth16 implementation
    # call the inspect_code function from filter/filterGroth16Contracts.py
    os.system(f"python filter/filterGroth16Contracts.py")

    # read the result from the csv file
    df = pd.read_csv(path)
    is_groth16 = df["is_groth16"][0]

    if is_groth16:
        print("The contract is a Groth16 implementation.")
        print("analyzing the contract...")
        pass
    else:
        print("======Report on this smart contract======")
        print("The contract is not a Groth16 implementation.")
        print("Execution completed.")
        print("=========================================")
        return
    
    # vulnerability detector
    # 1. check if SNARK scalar field and Prime Q are included in bytecode
    R_in_bytecode = SNARK_SCALAR_FIELD in bytecode
    Q_in_bytecode = PRIME_Q in bytecode
    # save to csv
    df["bytecode_has_R"] = R_in_bytecode
    df["bytecode_has_Q"] = Q_in_bytecode
    df.to_csv(path, index=False)
    
    # 2. decompile analysis
    os.system(f"python decompile/decompile.py")
    # read the result from the csv file
    df = pd.read_csv(path)
    is_decompile_complete = df["is_decompile_complete"][0]
    decompile_has_R =  df["decompile_has_R"][0]
    decompile_has_Q = df["decompile_has_Q"][0]

    # 3. simulator analysis
    os.system(f"python simulator/simulate.py")
    # read the result from the csv file
    df = pd.read_csv(path)
    simulator_has_R = df["simulator_has_R"][0]
    simulator_has_Q = df["simulator_has_Q"][0]

    # 4. decision making
    predict_has_R_constraint = False
    if not R_in_bytecode:
        predict_has_R_constraint = False
    else:
        if is_decompile_complete:
            predict_has_R_constraint = decompile_has_R or simulator_has_R
        else:
            predict_has_R_constraint = simulator_has_R or decompile_has_R
    
    predict_has_Q_constraint = False
    if not Q_in_bytecode:
        predict_has_Q_constraint = False
    else:
        if is_decompile_complete:
            predict_has_Q_constraint = decompile_has_Q or simulator_has_Q
        else:
            predict_has_Q_constraint = simulator_has_Q or decompile_has_Q
    # save new columns to the csv file
    df["predict_has_R_constraint"] = predict_has_R_constraint
    df["predict_has_Q_constraint"] = predict_has_Q_constraint
    df.to_csv(path, index=False)

    # 5. prototype analysis
    os.system(f"python classifier/classify.py")
    # read the result from the csv file
    df = pd.read_csv(path)
    prototype_name = df["prototype_name"][0]
    prototype_info = df["prototype_info"][0]
    prototype_address = df["prototype_address"][0]
    bytecode_fingerprint = df["bytecode_fingerprint"][0]

    # save report to a text file
    with open("output/report.txt", "w") as f:
        print("======Report on this smart contract======", file=f)
        print("-Vulnerability Prediction:", file=f)
        print("|----Has SNARK scalar field constraint?: {}".format(predict_has_R_constraint), file=f)
        print("|----Has Prime Q constraint?: {}".format(predict_has_Q_constraint), file=f)
        print("|", file=f)
        # print("-Bytecode Analysis:", file=f)
        # print("|----SNARK scalar field in bytecode: {}".format(R_in_bytecode), file=f)
        # print("|----Prime Q in bytecode: {}".format(Q_in_bytecode), file=f)
        # print("|", file=f)
        # print("-Decompile Analysis:", file=f)
        # print("|----Decompile complete: {}".format(is_decompile_complete), file=f)
        # print("|----SNARK scalar field in decompile: {}".format(decompile_has_R), file=f)
        # print("|----Prime Q in decompile: {}".format(decompile_has_Q), file=f)
        # print("|", file=f)
        # print("-Simulator Analysis:", file=f)
        # print("|----SNARK scalar field in simulator: {}".format(simulator_has_R), file=f)
        # print("|----Prime Q in simulator: {}".format(simulator_has_Q), file=f)
        print("|", file=f)
        print("-Prototype Analysis:", file=f)
        print("|----Contract fingerprint: {}".format(bytecode_fingerprint), file=f)
        print("|----Prototype name: {}".format(prototype_name), file=f)
        print("|----Prototype info: {}".format(prototype_info), file=f)
        print("|----Prototype address: {}".format(prototype_address), file=f)
        print("|", file=f)
        print("Execution completed.", file=f)
        print("=========================================", file=f)
    print("The report is saved to output/report.txt")
    # generate the report
    # print("======Report on this smart contract======")
    # print("-Vulnerability Prediction:")
    # print("|----Has SNARK scalar field constraint?: {}".format(predict_has_R_constraint))
    # print("|----Has Prime Q constraint?: {}".format(predict_has_Q_constraint))
    # print("-Bytecode Analysis:")
    # print("|----SNARK scalar field in bytecode: {}".format(R_in_bytecode))
    # print("|----Prime Q in bytecode: {}".format(Q_in_bytecode))
    # print("-Decompile Analysis:")
    # print("|----Decompile complete: {}".format(is_decompile_complete))
    # print("|----SNARK scalar field in decompile: {}".format(decompile_has_R))
    # print("|----Prime Q in decompile: {}".format(decompile_has_Q))
    # print("-Simulator Analysis:")
    # print("|----SNARK scalar field in simulator: {}".format(simulator_has_R))
    # print("|----Prime Q in simulator: {}".format(simulator_has_Q))
    # print("-Prototype Analysis:")
    # print("|----Contract fingerprint: {}".format(bytecode_fingerprint))
    # print("|----Prototype name: {}".format(prototype_name))
    # print("|----Prototype info: {}".format(prototype_info))
    # print("|----Prototype address: {}".format(prototype_address))
    # print("Execution completed.")
    # print("=========================================")
    

if __name__ == "__main__":
    main()
