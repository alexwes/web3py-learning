from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Solidity
compiled_sol = compile_standard(
    {
        'language' : 'Solidity',
        'sources' : {'SimpleStorage.sol': {'content': simple_storage_file}},
        'settings': {
            'outputSelection' : {
                "*" : {
                    '*' : ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open('compiled_code.json', 'w') as file:
    json.dump(compiled_sol, file)

# get bytecode

bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# get abi

abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/c6d14f5d54e844389fc70485f5849bdb"))
chain_id = 5
my_address = "0xb1d44A270349e6D5422D0fa09C8f7d7F562807F0"
private_key = os.getenv("PRIVATE_KEY")

# Create contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage.constructor().buildTransaction())
nonce = w3.eth.getTransactionCount(my_address)

# # Build txn
txn = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address, 
        "nonce": nonce
        })
signed_txn = w3.eth.account.sign_transaction(txn, private_key)

# Send txn

print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Working with the contract

ss = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(ss.functions.getInfo().call())
store_transaction = ss.functions.setName("Jolie", 19).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address, 
        "nonce": nonce+1
        })

signed_stored_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

print("Updating contract...")
tx_hash2 = w3.eth.send_raw_transaction(signed_stored_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash2)
print("Updated!")


print(ss.functions.getInfo().call())

