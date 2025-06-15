# Monad Testnet Swap Bot

This bot performs automated multi-token swaps on the Monad testnet using Web3 and Uniswap V2-style router. Each wallet swaps tokens in sequence (A → B → C → D) with random amounts and repeats the cycle 10 times.

## ✅ Requirements

- Python 3
- pip (Python package manager)
- Testnet wallets with MON and test tokens
- VPS or local machine

## 🔧 Setup Instructions (VPS)

1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip -y
   pip3 install web3
   ```

2. **Configure Wallets**
   Edit `wallets.json` and add your testnet wallet addresses and private keys:

   ```json
   [
     {
       "address": "0xYourWallet1",
       "private_key": "0xYourPrivateKey1"
     },
     {
       "address": "0xYourWallet2",
       "private_key": "0xYourPrivateKey2"
     }
   ]
   ```

3. **Run the Bot**
   ```bash
   python3 monad_swap_bot.py
   ```

4. **(Optional) Run as Cronjob**
   Open crontab:
   ```bash
   crontab -e
   ```

   Add this line to run every day at 4 AM:
   ```
   0 4 * * * /usr/bin/python3 /full/path/to/monad_swap_bot.py
   ```

## ⚠️ Notes

- Only use testnet wallets.
- Ensure your wallets have MON and tokens like USDC, USDT, WBTC, WETH.
- This script is for educational purposes only.

Happy farming 🚀
