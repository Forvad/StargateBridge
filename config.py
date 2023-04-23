import json
from web3 import Web3


# добавляем сюда рпс
polygon_rpc_url = 'https://polygon-rpc.com/'
avax_rpc_url = 'https://1rpc.io/avax/c'
bsc_rpc_url = 'https://bsc.rpc.blxrbdn.com'
ftm_rpc_url = 'https://rpcapi.fantom.network'


class ConfigZero:
    def __init__(self):
        # RPC
        self.polygon_w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))
        self.avax_w3 = Web3(Web3.HTTPProvider(avax_rpc_url))
        self.bsc_w3 = Web3(Web3.HTTPProvider(bsc_rpc_url))
        self.ftm_w3 = Web3(Web3.HTTPProvider(ftm_rpc_url))

        # Stargate Router
        self.stargate_polygon_address = self.polygon_w3.toChecksumAddress('0x45A01E4e04F14f7A4a6702c74187c5F6222033cd')
        self.stargate_avax_address = self.avax_w3.toChecksumAddress('0x45A01E4e04F14f7A4a6702c74187c5F6222033cd')
        self.stargate_bsc_address = self.bsc_w3.toChecksumAddress('0x4a364f8c717cAAD9A442737Eb7b8A55cc6cf18D8')
        self.stargate_ftm_address = self.ftm_w3.toChecksumAddress('0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6')
        self.woofy_avax_adress = self.avax_w3.toChecksumAddress('0x51AF494f1B4d3f77835951FA827D66fc4A18Dae8')

        # ABIs
        self.stargate_abi = json.load(open('router_abi.json'))
        self.usdc_abi = json.load(open('usdc_abi.json'))
        self.woofy_abi = json.load(open('woofy_abi.json'))

        # USDC contracts
        self.usdc_polygon_address = self.polygon_w3.toChecksumAddress('0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174')
        self.usdc_avax_address = self.avax_w3.toChecksumAddress('0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E')
        self.usdc_ftm_address = self.ftm_w3.toChecksumAddress('0x04068da6c83afcfa0e13ba15a6696662335d5b75')

        # USDT contracts
        self.usdt_avax_address = self.avax_w3.toChecksumAddress('0x55d398326f99059ff775485246999027b3197955')
        self.usdt_bsc_address = self.bsc_w3.toChecksumAddress('0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7')

        # Init contracts
        self.stargate_polygon_contract = self.polygon_w3.eth.contract(address=self.stargate_polygon_address,
                                                                      abi=self.stargate_abi)
        self.stargate_avax_contract = self.avax_w3.eth.contract(address=self.stargate_avax_address,
                                                                abi=self.stargate_abi)
        self.stargate_ftm_contract = self.ftm_w3.eth.contract(address=self.stargate_ftm_address,
                                                              abi=self.stargate_abi)
        self.woofy_avax_contract = self.avax_w3.eth.contract(address=self.woofy_avax_adress,
                                                             abi=self.woofy_abi)
        self.usdc_polygon_contract = self.polygon_w3.eth.contract(address=self.usdc_polygon_address,
                                                                  abi=self.usdc_abi)
        self.usdc_avax_contract = self.avax_w3.eth.contract(address=self.usdc_avax_address,
                                                            abi=self.usdc_abi)
        self.usdc_ftm_contract = self.ftm_w3.eth.contract(address=self.usdc_ftm_address,
                                                          abi=self.usdc_abi)
        self.usdt_bsc_contract = self.bsc_w3.eth.contract(address=self.usdt_bsc_address,
                                                          abi=self.usdc_abi)
        self.usdt_avax_contract = self.avax_w3.eth.contract(address=self.usdt_avax_address,
                                                            abi=self.usdc_abi)

        # Approved amount
        self.approved = 115792089237316195423570985008687907853269984665640564039457584007913129639935

        # Slippage
        self.slippage = 5



