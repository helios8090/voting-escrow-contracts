"""
Deployment Configuration file
=============================
This script holds customizeable / sensetive values related to the DAO deployment scripts.
See `README.md` in this directory for more information on how deployment works.
"""

from brownie import rpc, web3
from web3 import middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy as gas_strategy

DEPLOYMENTS_JSON = "deployments.json"
REQUIRED_CONFIRMATIONS = 3
TEST_DOP_TOKEN_ADDRESS = "0x5086fD4a18706Bf1b628179B2e8aA087d516eD35"
DOP_TOKEN_ADDRESS = ""

YEAR = 86400 * 365

def get_live_admin():
    # Admin and funding admin account objects used for in a live environment
    # May be created via accounts.load(name) or accounts.add(privkey)
    # https://eth-brownie.readthedocs.io/en/stable/account-management.html
    deployerId = "deployer"
    return deployerId


if not rpc.is_active():
    # logic that only executes in a live environment
    web3.eth.setGasPriceStrategy(gas_strategy)
    web3.middleware_onion.add(middleware.time_based_cache_middleware)
    web3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
    web3.middleware_onion.add(middleware.simple_cache_middleware)
