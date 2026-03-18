import os
import json
from datetime import datetime, timezone

from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

alchemy_url = os.getenv("ALCHEMY_URL")
if not alchemy_url:
    raise ValueError("Missing ALCHEMY_URL in .env")

w3 = Web3(Web3.HTTPProvider(alchemy_url))

if not w3.is_connected():
    raise ConnectionError("Could not connect to Ethereum RPC")

# -------- Addresses --------
STETH_ADDRESS = Web3.to_checksum_address("0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")
WSTETH_ADDRESS = Web3.to_checksum_address("0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0")

ASTETH_V2_ADDRESS = Web3.to_checksum_address("0x1982b2F5814301d4e9a8b0201555376e62F82428")
A_WSTETH_V3_ADDRESS = Web3.to_checksum_address("0x0B925eD163218f6662a35e0f0371Ac234f9E9371")

# -------- Minimal ERC20 ABI --------
ERC20_ABI = [
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


def get_token_snapshot(token_address: str) -> dict:
    contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)

    name = contract.functions.name().call()
    symbol = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()
    total_supply_raw = contract.functions.totalSupply().call()
    total_supply = total_supply_raw / (10 ** decimals)

    return {
        "address": token_address,
        "name": name,
        "symbol": symbol,
        "decimals": decimals,
        "total_supply_raw": total_supply_raw,
        "total_supply": total_supply,
    }


def main():
    timestamp = datetime.now(timezone.utc).isoformat()

    steth = get_token_snapshot(STETH_ADDRESS)
    wsteth = get_token_snapshot(WSTETH_ADDRESS)
    a_steth_v2 = get_token_snapshot(ASTETH_V2_ADDRESS)
    a_wsteth_v3 = get_token_snapshot(A_WSTETH_V3_ADDRESS)

    aave_v2_percent_of_steth = (a_steth_v2["total_supply"] / steth["total_supply"]) * 100
    aave_v3_percent_of_wsteth = (a_wsteth_v3["total_supply"] / wsteth["total_supply"]) * 100

    print("----- Track 1: Lido × Aave Monitoring Layer -----")
    print(f"Timestamp (UTC): {timestamp}")
    print()

    print(f"Base asset 1: {steth['name']} ({steth['symbol']})")
    print(f"Address: {steth['address']}")
    print(f"Total supply: {steth['total_supply']:,.2f}")
    print()

    print(f"Base asset 2: {wsteth['name']} ({wsteth['symbol']})")
    print(f"Address: {wsteth['address']}")
    print(f"Total supply: {wsteth['total_supply']:,.2f}")
    print()

    print(f"Tracked Aave V2 token: {a_steth_v2['name']} ({a_steth_v2['symbol']})")
    print(f"Address: {a_steth_v2['address']}")
    print(f"Total supply: {a_steth_v2['total_supply']:,.2f}")
    print()

    print(f"Tracked Aave V3 token: {a_wsteth_v3['name']} ({a_wsteth_v3['symbol']})")
    print(f"Address: {a_wsteth_v3['address']}")
    print(f"Total supply: {a_wsteth_v3['total_supply']:,.2f}")
    print()

    print("----- Summary Metrics -----")
    print(f"Aave V2 stETH exposure: {a_steth_v2['total_supply']:,.2f} stETH")
    print(f"Aave V2 share of total stETH supply: {aave_v2_percent_of_steth:.4f}%")
    print()
    print(f"Aave V3 wstETH exposure: {a_wsteth_v3['total_supply']:,.2f} wstETH")
    print(f"Aave V3 share of total wstETH supply: {aave_v3_percent_of_wsteth:.4f}%")

    result = {
        "timestamp_utc": timestamp,
        "steth_total_supply": steth["total_supply"],
        "wsteth_total_supply": wsteth["total_supply"],
        "aave_v2_steth_supply": a_steth_v2["total_supply"],
        "aave_v2_percent_of_steth": aave_v2_percent_of_steth,
        "aave_v3_wsteth_supply": a_wsteth_v3["total_supply"],
        "aave_v3_percent_of_wsteth": aave_v3_percent_of_wsteth,
    }

    with open("track1_snapshot.json", "w") as f:
        json.dump(result, f, indent=2)

    print()
    print("----- Reusable Result Object -----")
    print(result)
    print()
    print("Saved snapshot to track1_snapshot.json")


if __name__ == "__main__":
    main()