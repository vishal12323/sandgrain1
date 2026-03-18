import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

alchemy_url = os.getenv("ALCHEMY_URL")
if not alchemy_url:
    raise ValueError("Missing ALCHEMY_URL in .env")

w3 = Web3(Web3.HTTPProvider(alchemy_url))

if not w3.is_connected():
    raise ConnectionError("Could not connect to Ethereum RPC")

print("Connected to chain ID:", w3.eth.chain_id)

token_address = Web3.to_checksum_address("0x1982b2F5814301d4e9a8b0201555376e62F82428")
steth_address = Web3.to_checksum_address("0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")

erc20_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    }
]

steth = w3.eth.contract(address=steth_address, abi=erc20_abi)
token = w3.eth.contract(address=token_address, abi=erc20_abi)

steth_supply_raw = steth.functions.totalSupply().call()
steth_decimals = steth.functions.decimals().call()
steth_symbol = steth.functions.symbol().call()
steth_name = steth.functions.name().call()

token_supply_raw = token.functions.totalSupply().call()
token_decimals = token.functions.decimals().call()
token_symbol = token.functions.symbol().call()
token_name = token.functions.name().call()

steth_supply = steth_supply_raw / (10 ** steth_decimals)
token_supply = token_supply_raw / (10 ** token_decimals)

percent = (token_supply / steth_supply) * 100

print("\n----- Token Inspection -----")
print(f"stETH name: {steth_name}")
print(f"stETH symbol: {steth_symbol}")
print(f"stETH decimals: {steth_decimals}")
print(f"stETH total supply: {steth_supply:,.2f}")

print()
print(f"Tracked token address: {token_address}")
print(f"Tracked token name: {token_name}")
print(f"Tracked token symbol: {token_symbol}")
print(f"Tracked token decimals: {token_decimals}")
print(f"Tracked token total supply: {token_supply:,.2f}")

print("\n----- Concentration Snapshot -----")
print(f"{token_symbol} / {steth_symbol} supply ratio: {percent:.4f}%")