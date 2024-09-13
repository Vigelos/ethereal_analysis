import os
import time
import pandas as pd
import argparse
from web3 import Web3


END_POINTS = {
    "Merkle": "https://eth.merkle.io",
    #"Name": "URL"
}

def merge_csv(source_dir, dest_dir, file_name):
    files = os.listdir(source_dir)
    # filter out non-csv files
    files = [f for f in files if f.endswith(".csv")]
    df = pd.concat([pd.read_csv(os.path.join(source_dir, f)) for f in files])

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

def scan_blocks_web3(start_block_number, end_block_number, endpoint, endpoint_name):
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
    df.to_csv("{}/{:08d}_to_{:08d}.csv".format(endpoint_name, start_block_number, end_block_number), index=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", type=str, help="The endpoint to use for the scan", default="Merkle")
    parser.add_argument("--startId", type=int, help="The block to start scanning", default=0)
    parser.add_argument("--endId", type=int, help="The block to end scanning", default=20000000)
    args = parser.parse_args()
    endpoint = Web3(Web3.HTTPProvider(END_POINTS[args.endpoint]))
    start_block_number = args.startId
    end_block_number = args.endId
    print("start scanning from block {} to block {}".format(start_block_number, end_block_number))
    
    if not os.path.exists("{}".format(args.endpoint)):
        os.makedirs("{}".format(args.endpoint))
        if end_block_number - start_block_number < 100:
            scan_blocks_web3(start_block_number, end_block_number, endpoint, args.endpoint)
        else:
            for i in range(start_block_number, end_block_number, 100):
                scan_blocks_web3(i, i+100 if i+100 < end_block_number else end_block_number, endpoint, args.endpoint)
            merge_csv(args.endpoint, ".", "{:08d}_to_{:08d}.csv".format(start_block_number, end_block_number))

if __name__ == "__main__":
    main()