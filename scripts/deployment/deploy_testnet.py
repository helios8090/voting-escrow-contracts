# Testnet deployment script

import json
import time

from brownie import (
    VotingEscrow,
    FeeDistributor,
    accounts,
)

from . import deployment_config as config

USE_STRATEGIES = False  # Needed for the ganache-cli tester which doesn't like middlewares
POA = True

DEPLOYER = "0x1aeBc84042d8Fd415bBa14d25597B4C2748D52Eb"
DEPLOYER_ID = "deployer"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


CONFS = 1


def repeat(f, *args):
    """
    Repeat when geth is not broadcasting (unaccounted error)
    """
    while True:
        try:
            return f(*args)
        except KeyError:
            continue


def save_abi(contract, name):
    with open("%s.abi" % name, "w") as f:
        json.dump(contract.abi, f)

def main():
    # unlock key file
    deployerId = config.get_live_admin()
    deployerAddress = accounts.load(deployerId)
    deployer = accounts.at(deployerAddress)

    # deploy votingEscrow and feeDistributor
    print(f"Deploying from {deployer}")
    escrow = repeat(
        VotingEscrow.deploy,
        config.TEST_DOP_TOKEN_ADDRESS,
        "Vote-escrowed DOP",
        "veDOP",
        "veDOP_1.00",
        {"from": deployer, "required_confs": CONFS},
    )
    save_abi(escrow, "voting_escrow")

    feeDistributor = repeat(
        FeeDistributor.deploy,
        escrow,
        0, # start time
        config.TEST_DOP_TOKEN_ADDRESS,
        deployer,
        deployer,
        {"from": deployer, "required_confs": CONFS},
    )
    save_abi(feeDistributor, "fee_distributor")
    
