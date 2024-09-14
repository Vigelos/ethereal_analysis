## Ethereum smart contract scanner and analysis

This is the tool developed as a part of my master thesis *Hunting Vulnerabilities in Groth16 zk-SNARK implemented by Ethereum Smart Contracts*. 

This tool includes:
> - A scanner to download smart contracts from Etherum history blocks.
> - A tool to detect whether a Groth16 contract is susceptible to **Missing constraint on public inputs** vulnerability.

### Block scanner
The block scanner scan all visible contracts from given Ethereum blocks. To include all visiable and invisible contracts, we recommend using https://github.com/paradigmxyz/cryo .


##### Installation
- Install Dependence
```pip install os time pandas argparse web3```
- Config RPC Endpoints

Copy the url of you won RPC endpoint to `scanner/get_contracts.py`
```
END_POINTS = {
"Merkle":"https://eth.merkle.io",
"Your Endpoint Name": "Your URL"
}
```
##### Example Usage
For example, if you want to download smart contract from block 18,000,000 to 18,000,123, you cna use the following command:
```
cd scanner
python get_contracts.py --startId 18000000 --endId 18000123 --endpoint <your endpoint name>
```
The download contracts will be listed in a .csv file, where the format is [block_id, contract_address, bytecode]

---

### Vulnerability Analyser
This tool inspect the bytecode of a given Groth16 smart contract to see if there exist the vulnerability of missing constraint check on public inputs, specifically:
> - public variables, like nullifier hash should be constrained to be smaller than SNARK scalar field.
> - Groth16 proofs (A,B,C) should be constrained to be smaller than prime Q.
##### Installation
- Install Dependence

This tool has dependence on Heimdall, you need to install Heimdall first. https://github.com/linuxserver/Heimdall

And the following python libraries:
```pip install pandas argparse os pyevmasm time```

##### Example Usage
```
cd analysis
python main.py --bytecode <bytecode of the target smart contract>
```
terminal output
```
The contract is a Groth16 implementation.
analyzing the contract...
The report is saved to output/report.txt
```
in `output/report.txt`
```
======Report on this smart contract======
-Vulnerability Prediction:
|----Has SNARK scalar field constraint?: False
|----Has Prime Q constraint?: True
|
|
-Prototype Analysis:
|----Contract fingerprint: QBAQC
|----Prototype name: snarkjs
|----Prototype info: The prototype may be vulnerable due to incorrect [public_input < snark_scalar_field] check and missing [proof < prime_Q] check. For more information, please refer to https://github.com/iden3/snarkjs/pull/480
|----Prototype address: 0xEB2952A4098e15C97E1Ce126FE479f27E2FFB40c
|
Execution completed.
=========================================
```