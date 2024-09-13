import re
import pandas as pd

FINGER_PRINTS = {
    # Gas, Sub, Staticcall 0x06
    "60066107d05a03fa": "A",
    # Gas, Sub, Staticcall 0x07
    "60076107d05a03fa": "B",
    # Gas, Sub, Staticcall 0x08
    "60086107d05a03fa": "C",

    # Prime Q
    "30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47":"Q",
    # SNARK scalar field
    "30644e72e131a029b85045b68181585d2833e84879b9709143e1f593f0000001":"R"
}

def find_pattern_indices(bytecode, pattern):
    # find the indices of a pattern in the bytecode
    indices = []
    start = 0
    while True:
        index = bytecode.find(pattern, start)
        if index == -1:  # Pattern not found
            break
        indices.append(index)
        start = index + len(pattern)  # Move past the last found occurrence
    return indices

def get_finger_print(bytecode):

    finger_print = []

    for pattern, name in FINGER_PRINTS.items():
        indices = find_pattern_indices(bytecode, pattern)
        indices = [(index, name) for index in indices]
        finger_print.extend(indices)
    
    # sort the fingerprint by index
    finger_print.sort(key=lambda x: x[0])
    finger_print = [name for index, name in finger_print]

    return "".join(finger_print)


class Contract:
    def __init__(self, bytecode, predict_scalar, predict_prime):
        self.bytecode = bytecode
        self.predict_scalar = predict_scalar
        self.predict_prime = predict_prime
        self.finger_print = get_finger_print(bytecode)

        if (self.finger_print in ["BACQ","BACQR"]) and (not self.predict_scalar) and (not self.predict_prime):
            self.prototype = "Exitor"
            self.address = "0xa756079526E2fB008290b93D65E297ADe6FE5e03"
            self.info = "The prototype may be vulnerable due to Missing [public_input < snark_scalar_field] check and [proof < prime_Q] check"
            return
        
        if (self.finger_print == "BACQRRR") and (not self.predict_scalar) and (not self.predict_prime):
            self.prototype = "Mixer.v1"
            self.address = "0xfdc0Eb098a6D27cA62BB67e0804D461cB698f9fA"
            self.info = "The prototype may be vulnerable due to Missing [public_input < snark_scalar_field] check and [proof < prime_Q] check"
            return
        
        if (self.finger_print == "RBACCQRBBABAB") and ( self.predict_scalar ) and (not self.predict_prime):
            self.prototype = "Loopring"
            self.address = "0x40598B41cc17a7E56dd72F415E8223aaCCA94cF7"
            self.info = "The prototype may be vulnerable due to Missing [proof < prime_Q] check"
            return
        
        if (self.finger_print == "QQCBAR"):
            self.prototype = "Zeropool"
            self.address = "0x00813626695bD9cBaB357eEDD45E5083311eDEaa"
            self.info = "The prototype may be vulnerable due to Missing [proof < prime_Q] check"
            return
        
        if (self.finger_print in ["RRRRRRRRRRRRRRRBAQQQQQQC","RRRRRRBAQQQQQQC","RRRRRRRBAQQQQQQC"]):
            self.prototype = "Railgun"
            self.address = "0xc6368d9998Ea333B37Eb869F4E1749B9296e6d09"
            self.info = "The prototype may be vulnerable due to Missing [proof < prime_Q] check"
            return
        
        if (self.finger_print == "QRBAQQC") and (self.predict_scalar) and (self.predict_prime):
            self.prototype = "Tornado"
            self.address = "0x09193888b3f38C82dEdfda55259A82C0E7De875E"
            self.info = ""
            return
        
        if (self.finger_print in ["QBAQC","QBAQQC","QBAQQCRRRRR"]) and (not self.predict_scalar) and (self.predict_prime):
            self.prototype = "snarkjs"
            self.address = "0xEB2952A4098e15C97E1Ce126FE479f27E2FFB40c"
            self.info = "The prototype may be vulnerable due to incorrect [public_input < snark_scalar_field] check and missing [proof < prime_Q] check. For more information, please refer to https://github.com/iden3/snarkjs/pull/480"
            return
        
        self.prototype = "Unknown Prototype"
        self.address = ""
        self.info = ""