from time import sleep
import config
from web3.exceptions import TransactionNotFound


class ZeroBridge:
    def __init__(self, pr_key: str):
        self.privat_key = pr_key
        self.configs = config.ConfigZero()
        self.address = self.configs.polygon_w3.eth.account.from_key(self.privat_key).address

    # Polygon -> Avax(106), FTM(112) USDC Bridge
    def polygon_to(self, amount: (int, float), min_amount: (int, float), network: str) -> bool:
        self.checking_balance('Polygon', amount)
        network_id = {'Avax': 106, 'FTM': 112}
        nonce = self.configs.polygon_w3.eth.get_transaction_count(self.address)
        gas_price = self.configs.polygon_w3.eth.gas_price
        fee = self.configs.stargate_polygon_contract.functions.quoteLayerZeroFee(network_id[network],
                                                                     1,
                                                                     "0x0000000000000000000000000000000000001010",
                                                                     "0x",
                                                                     [0, 0,
                                                                      "0x0000000000000000000000000000000000000001"]
                                                                     ).call()[0]

        # Check allowance
        allowance = self.configs.usdc_polygon_contract.functions.allowance(
            self.address, self.configs.stargate_polygon_address).call()
        if allowance < amount:
            approve_txn = self.configs.usdc_polygon_contract.functions.approve(
                self.configs.stargate_polygon_address, self.configs.approved).buildTransaction(
                {
                    'from': self.address,
                    'gas': 150000,
                    'gasPrice': gas_price,
                    'nonce': nonce,
                })
            signed_approve_txn = self.configs.polygon_w3.eth.account.sign_transaction(approve_txn, self.privat_key)
            approve_txn_hash = self.configs.polygon_w3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)

            print(f"POLYGON | USDС APPROVED https://polygonscan.com/tx/{approve_txn_hash.hex()}")
            nonce += 1

            sleep(60)

        # Stargate Swap
        chainId = network_id[network]
        source_pool_id = 1
        dest_pool_id = 1
        refund_address = self.address
        amountIn = amount
        amountOutMin = min_amount
        lzTxObj = [0, 0, '0x0000000000000000000000000000000000000001']
        to = self.address
        data = '0x'

        swap_txn = self.configs.stargate_polygon_contract.functions.swap(
            chainId, source_pool_id, dest_pool_id, refund_address, amountIn, amountOutMin, lzTxObj, to, data
        ).buildTransaction({
            'from': self.address,
            'value': fee,
            'gas': 500000,
            'gasPrice': self.configs.polygon_w3.eth.gas_price,
            'nonce': self.configs.polygon_w3.eth.get_transaction_count(self.address),
        })

        signed_swap_txn = self.configs.polygon_w3.eth.account.sign_transaction(swap_txn, self.privat_key)
        swap_txn_hash = self.configs.polygon_w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        sleep(60)
        txn = self.checking_txn(self.configs.polygon_w3, swap_txn_hash.hex())
        if txn:
            print(f"Transaction: https://polygonscan.com/tx/{swap_txn_hash.hex()}")
            return True
        else:
            return False

    # Avax -> Polygon(109), Fantom(112) USDC
    def avax_to(self, amount: int, min_amount: int, network: str) -> bool:
        network_id = {'Polygon': 109, 'FTM': 112}

        self.checking_balance('Avax', amount)
        nonce = self.configs.avax_w3.eth.get_transaction_count(self.address)
        gas_price = self.configs.avax_w3.eth.gas_price
        fee = self.configs.stargate_avax_contract.functions.quoteLayerZeroFee(network_id[network],
                                                                               1,
                                                                        "0x0000000000000000000000000000000000000001",
                                                                               "0x",
                                                                    [0, 0, "0x0000000000000000000000000000000000000001"]
                                                                  ).call()[0]

        # Check Allowance
        allowance = self.configs.usdc_avax_contract.functions.allowance(
            self.address, self.configs.stargate_avax_address).call()
        if allowance < amount:
            approve_txn = self.configs.usdc_avax_contract.functions.approve(
                self.configs.stargate_avax_address, self.configs.approved).buildTransaction({
                    'from': self.address,
                    'gas': 150000,
                    'gasPrice': gas_price,
                    'nonce': nonce,
                })
            signed_approve_txn = self.configs.avax_w3.eth.account.sign_transaction(approve_txn, self.privat_key)
            approve_txn_hash = self.configs.avax_w3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)

            print(f"AVAX | USDC APPROVED | https://snowtrace.io/tx/{approve_txn_hash.hex()} ")
            nonce += 1

            sleep(60)

            # Stargate Swap
        chainId = network_id[network]
        source_pool_id = 1
        dest_pool_id = 1
        refund_address = self.address
        amountIn = amount
        amountOutMin = min_amount
        lzTxObj = [0, 0, '0x0000000000000000000000000000000000000001']
        to = self.address
        data = '0x'

        swap_txn = self.configs.stargate_avax_contract.functions.swap(
            chainId, source_pool_id, dest_pool_id, refund_address, amountIn, amountOutMin, lzTxObj, to, data
        ).buildTransaction({
            'from': self.address,
            'value': fee,
            'gas': 600000,
            'gasPrice': self.configs.avax_w3.eth.gas_price,
            'nonce': self.configs.avax_w3.eth.get_transaction_count(self.address),
        })

        signed_swap_txn = self.configs.avax_w3.eth.account.sign_transaction(swap_txn, self.privat_key)
        swap_txn_hash = self.configs.avax_w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        sleep(60)
        txn = self.checking_txn(self.configs.avax_w3, swap_txn_hash.hex())
        if txn:
            print(f"Transaction: https://snowtrace.io/tx/{swap_txn_hash.hex()}")
            return True
        else:
            return False

    def ftm_to(self, amount: (int, float), min_amount: (int, float), network: str) -> bool:
        network_id = {'Polygon': 109, 'Avax': 106}

        self.checking_balance('FTM', amount)
        nonce = self.configs.ftm_w3.eth.get_transaction_count(self.address)
        gas_price = self.configs.ftm_w3.eth.gas_price
        fee = self.configs.stargate_ftm_contract.functions.quoteLayerZeroFee(network_id[network],
                                                                               1,
                                                                        "0x0000000000000000000000000000000000000001",
                                                                               "0x",
                                                                    [0, 0, "0x0000000000000000000000000000000000000001"]
                                                                  ).call()[0]

        # Check Allowance
        allowance = self.configs.usdc_ftm_contract.functions.allowance(self.address, self.configs.stargate_ftm_address)\
            .call()
        if allowance < amount:
            approve_txn = self.configs.usdc_ftm_contract.functions.approve(
                self.configs.stargate_ftm_address, self.configs.approved).buildTransaction({
                    'from': self.address,
                    'gas': 150000,
                    'gasPrice': gas_price,
                    'nonce': nonce
                })
            signed_approve_txn = self.configs.ftm_w3.eth.account.sign_transaction(approve_txn, self.privat_key)
            approve_txn_hash = self.configs.ftm_w3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)

            print(f"FANTOM | USDC APPROVED | https://ftmscan.com/tx/{approve_txn_hash.hex()} ")
            nonce += 1

            sleep(60)

            # Stargate Swap
        chainId = network_id[network]
        source_pool_id = 1
        dest_pool_id = 1
        refund_address = self.address
        amountIn = amount
        amountOutMin = min_amount
        lzTxObj = [0, 0, '0x0000000000000000000000000000000000000001']
        to = self.address
        data = '0x'

        swap_txn = self.configs.stargate_ftm_contract.functions.swap(
            chainId, source_pool_id, dest_pool_id, refund_address, amountIn, amountOutMin, lzTxObj, to, data
        ).buildTransaction({
            'from': self.address,
            'value': fee,
            'gas': 550000,
            'gasPrice': self.configs.ftm_w3.eth.gas_price,
            'nonce': self.configs.ftm_w3.eth.get_transaction_count(self.address),
        })

        signed_swap_txn = self.configs.ftm_w3.eth.account.sign_transaction(swap_txn, self.privat_key)
        swap_txn_hash = self.configs.ftm_w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        sleep(60)
        txn = self.checking_txn(self.configs.ftm_w3, swap_txn_hash.hex())
        if txn:
            print(f"Transaction: https://ftmscan.com/tx/{swap_txn_hash.hex()}")
            return True
        else:
            return False

    def balance(self):
        return {'Polygon': self.configs.usdc_polygon_contract.functions.balanceOf(self.address).call() / (10 ** 6),
                'Avax': self.configs.usdc_avax_contract.functions.balanceOf(self.address).call() / (10 ** 6),
                'FTM': self.configs.usdc_ftm_contract.functions.balanceOf(self.address).call() / (10 ** 6)}

    def checking_balance(self, network: str, amount: (int, float)):
        balance = self.balance()[network]
        if amount / (1 * 10 ** 6) > balance:
            raise f'Ваш баланс({balance}) меньше назначеной суммы({amount}) '

    @staticmethod
    def checking_txn(w3, swap_txn):
        try:
            txn_info = w3.eth.get_transaction_receipt(swap_txn)['status']
            if txn_info:
                return True
            else:
                return False
        except TransactionNotFound:
            return False


def wallet():
    with open('wallet.txt', 'r') as f:
        wallets = f.read().splitlines()
        return wallets


def main():
    wallets = wallet()
    for wall in wallets:
        bridge = ZeroBridge(wall)
        amount_ = bridge.balance()['Avax'] * (10 ** 6)
        if amount_ <= 0:
            raise 'баланс равен нулю'
        min_amount = amount_ - (amount_ * 5) // 1000

        # Bridge AVAX to Fantom

        circle = 0
        while circle < 3:
            if bridge.avax_to(int(amount_), int(min_amount), 'FTM'):
                while True:
                    if bridge.balance()['FTM'] >= min_amount / (10 ** 6):
                        amount_ = bridge.balance()['FTM'] * (10 ** 6)
                        break
                    else:
                        sleep(60)
                break
            circle += 1

        # Bridge Fantom to Polygon

        circle = 0
        while circle < 3:
            if bridge.ftm_to(int(amount_), int(min_amount), 'Polygon'):
                while True:
                    if bridge.balance()['Polygon'] >= min_amount / (10 ** 6):
                        amount_ = bridge.balance()['Polygon'] * (10 ** 6)
                        break
                    else:
                        sleep(60)
                break
            circle += 1

        # Bridge Polygon to Avax

        circle = 0
        while circle < 3:
            if bridge.polygon_to(int(amount_), int(min_amount), 'Avax'):
                print(f'Account {bridge.address} is ready')
                break
            circle += 1

        sleep(300)


if __name__ == '__main__':
    main()
