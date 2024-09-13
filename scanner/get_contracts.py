import os
import time
import pandas as pd
import argparse
from web3 import Web3


END_POINTS = {
    "Merkle": "https://eth.merkle.io", # normal
    "Ankr": "https://rpc.ankr.com/eth/6be4700d61bcc2c4fecf4dbbfcab2e672dd2df20584017477d7628debfdc50f4", # normal
    "Alchemy": "https://eth-mainnet.g.alchemy.com/v2/8fQ58AhCoTWRQK8WT_PV0tH79wnTrJ99",
    "Llama": "https://eth.llamarpc.com", # slow
    "Tenderly": "https://mainnet.gateway.tenderly.co/5G6snCXHXFCDCv3S5PjluA", # very fast
    "DRPC": "https://lb.drpc.org/ogrpc?network=ethereum&dkey=Asdkjr1IPUcBk0up5DK-s_rjUIfcNTcR76SyhkHL9tz4", # very fast
    "ChainNode": "https://mainnet.chainnodes.org/d5e5cf0f-10be-4742-8b1a-779ae47b37e7", # very fast
    "OnFinality": "https://eth.api.onfinality.io/public", # slow
    "Infura": "https://mainnet.infura.io/v3/75b7bcce439246a18c6d879e0692fbf5" # normal
}

def merge_csv(source_dir, dest_dir, file_name):
    files = os.listdir(source_dir)
    # filter out non-csv files
    files = [f for f in files if f.endswith(".csv")]
    df = pd.concat([pd.read_csv(os.path.join(source_dir, f)) for f in files])

    # if the same name already exists, ask for confirmation
    # if os.path.exists(os.path.join(dest_dir, file_name)):
    #     print("The file {} already exists. Do you want to overwrite it?".format(file_name))
    #     choice = input("Enter y/n: ")
    #     if choice != "y":
    #         return

    df.to_csv(os.path.join(dest_dir, file_name), index=False)
    
    # clear the source directory
    os.system("rm -rf {}/*".format(source_dir))

def get_contract_address_web3(hash, endpoint):
    while True:
        try:
            respond = endpoint.eth.get_transaction_receipt(hash)
            return respond['contractAddress']
        except Exception as e:
            print(f"Error fetching transaction receipt: {e}, sleep 1s to comply with rate limit")
            time.sleep(1)

def get_code_web3(address, block_id, endpoint):
    # max retry 5 times
    retry = 0
    while True:
        try:
            respond = endpoint.eth.get_code(Web3.to_checksum_address(address), block_id).hex()
            return respond
        except Exception as e:
            # print(f"Error fetching contract code: {e}, sleep 1s to comply with rate limit")
            time.sleep(1)
            retry += 1
            if retry == 5:
                print(f"Error fetching contract code: {e}, skip this contract")
                return "0x"

def scan_blocks_web3(start_block_number, end_block_number, endpoint):
    creation_transactions = []

    for block_id in range(start_block_number, end_block_number):
        
        while True:
            try:
                block = endpoint.eth.get_block(hex(block_id), True)
                break
            except Exception as e:
                print(f"Error fetching block: {e}, sleep 1s to comply with rate limit")
                time.sleep(1)
        
        for tx in block['transactions']:
            if tx['to'] is None:
                address = get_contract_address_web3(tx['hash'], endpoint)
                code = get_code_web3(address, tx['blockNumber'], endpoint)
                if code != "0x":
                    creation_transactions.append((
                        tx['blockNumber'],
                        tx['hash'].hex(),
                        address,
                        code
                    ))
                
    # save the creation_transactions to a csv file
    df = pd.DataFrame(creation_transactions, columns=["block_number", "transaction_hash", "contract_address", "code"])
    df.to_csv("e2_{}/{:08d}_to_{:08d}.csv".format(args.endpoint, start_block_number, end_block_number), index=False)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", type=str, help="The endpoint to use for the scan", default="Merkle")
    parser.add_argument("--M", type=int, help="The x M block", default=0)
    parser.add_argument("--e4Start", type=int, help="start from x0,000 block", default=0)
    parser.add_argument("--e4End", type=int, help="end at y0,000 block", default=100)
    parser.add_argument("--offset", type=int, help="The offset to continue", default=0)

    args = parser.parse_args()

    # get the endpoint
    endpoint = Web3(Web3.HTTPProvider(END_POINTS[args.endpoint]))

    if args.offset != 0:
        use_offset = True
    else:
        use_offset = False

    # create the output directory if not exists
    if not os.path.exists("e2_{}".format(args.endpoint)):
        os.makedirs("e2_{}".format(args.endpoint))

    for e4 in range(args.e4Start, args.e4End):
        t1 = time.time()

        for i in range(args.offset if use_offset else 0,100):
            start_block_number = args.M*1000000 + e4*10000 + i * 100
            end_block_number = start_block_number + 100
            scan_blocks_web3(start_block_number, end_block_number, endpoint)
        
        merge_csv("e2_{}".format(args.endpoint), "e4", "{:08d}_to_{:08d}.csv".format(args.M*1000000 + e4*10000 + (args.offset*100 if use_offset else 0), args.M*1000000 + e4*10000+10000))
        print("scannered {} to {} in {} minutes".format(args.M*1000000 + e4*10000, args.M*1000000 + e4*10000+10000 , int((time.time()-t1)/60)))
        use_offset = False

