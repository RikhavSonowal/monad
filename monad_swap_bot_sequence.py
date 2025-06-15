import json
import time
from web3 import Web3

# ============ CONFIGURATION ============ #
RPC_URL = "https://testnet-rpc.monad.xyz"
ROUTER_CONTRACT_ADDRESS = "0xfb8e1c3b833f9e67a71c859a132cf783b645e436"

# Token addresses (Example: USDT, USDC, WBTC, WETH on Monad Testnet)
TOKEN_A = "0x88b8E2161DEDC77EF4ab7585569D2415a1C1055D"  # USDT
TOKEN_B = "0xf817257fed379853cDe0fa4F97AB987181B1E5Ea"  # USDC
TOKEN_C = "0xcf5a6076cfa32686c0Df13aBaDa2b40dec133F1d"  # WBTC
TOKEN_D = "0xB5a30b0FDc5EA94A52fDc42e3E9760Cb8449Fb37"  # WETH

SWAP_PATHS = [
    [TOKEN_A, TOKEN_B],
    [TOKEN_B, TOKEN_C],
    [TOKEN_C, TOKEN_D],
    [TOKEN_D, TOKEN_C],
    [TOKEN_D, TOKEN_B],
    [TOKEN_D, TOKEN_A],
    [TOKEN_C, TOKEN_B],
    [TOKEN_C, TOKEN_A],
    [TOKEN_B, TOKEN_D],
    [TOKEN_B, TOKEN_A]
]

TOKENS = [TOKEN_A, TOKEN_B, TOKEN_C, TOKEN_D]

web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Minimal ABI for Uniswap V2 Router swapExactTokensForTokens
ROUTER_ABI = [
    {
        "name": "swapExactTokensForTokens",
        "type": "function",
        "inputs": [
            {"name": "amountIn", "type": "uint256"},
            {"name": "amountOutMin", "type": "uint256"},
            {"name": "path", "type": "address[]"},
            {"name": "to", "type": "address"},
            {"name": "deadline", "type": "uint256"}
        ],
        "outputs": [{"name": "", "type": "uint256[]"}],
        "stateMutability": "nonpayable"
    }
]

ERC20_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]

router = web3.eth.contract(address=ROUTER_CONTRACT_ADDRESS, abi=ROUTER_ABI)

# Sequence-based amount loop
AMOUNTS = [0.01, 0.02, 0.03, 0.04, 0.05]
amount_index = 0

def random_amount():
    global amount_index
    amount = AMOUNTS[amount_index]
    amount_index = (amount_index + 1) % len(AMOUNTS)
    return amount

def approve_tokens(wallet, tokens):
    try:
        acct = web3.eth.account.from_key(wallet["private_key"])
        nonce = web3.eth.get_transaction_count(wallet["address"])
        for token in tokens:
            token_contract = web3.eth.contract(address=token, abi=ERC20_ABI)
            tx = token_contract.functions.approve(
                ROUTER_CONTRACT_ADDRESS, web3.to_wei(1000, 'ether')
            ).build_transaction({
                'from': wallet["address"],
                'nonce': nonce,
                'gas': 60000,
                'gasPrice': web3.to_wei('2', 'gwei')
            })
            signed = acct.sign_transaction(tx)
            tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
            print(f"✅ Approved {token[:6]}... for {wallet['address']}: {tx_hash.hex()}")
            nonce += 1
            time.sleep(5)
    except Exception as e:
        print(f"❌ Approve error for {wallet['address']}: {str(e)}")

def perform_multi_swap(wallet):
    try:
        acct = web3.eth.account.from_key(wallet["private_key"])
        nonce = web3.eth.get_transaction_count(wallet["address"])
        for cycle in range(10):
            print(f"➡️ Cycle {cycle+1}/10 for {wallet['address']}")
            for path in SWAP_PATHS:
                amt = random_amount()
                tx = router.functions.swapExactTokensForTokens(
                    web3.to_wei(amt, 'ether'), 0, path, wallet["address"],
                    int(time.time()) + 600
                ).build_transaction({
                    'from': wallet["address"], 'nonce': nonce,
                    'gas': 200000, 'gasPrice': web3.to_wei('2', 'gwei')
                })
                signed = acct.sign_transaction(tx)
                txh = web3.eth.send_raw_transaction(signed.rawTransaction)
                print(f"🔁 {path[0]}→{path[1]} {amt} MON: {txh.hex()}")
                nonce += 1
                time.sleep(10)
            time.sleep(30)
    except Exception as e:
        print(f"❌ Error for {wallet['address']}: {str(e)}")

if __name__ == "__main__":
    with open("wallets.json") as f:
        WALLETS = json.load(f)
    for w in WALLETS:
        approve_tokens(w, TOKENS)
        perform_multi_swap(w)
