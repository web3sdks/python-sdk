from web3sdks.core.classes.ipfs_storage import IpfsStorage
from web3sdks.core.classes.registry import ContractRegistry
from web3sdks.core.classes.factory import ContractFactory
from web3.middleware import geth_poa_middleware
from web3sdks.core.sdk import Web3sdksSDK
from eth_account import Account
from dotenv import load_dotenv
from web3 import Web3
import pytest
import os

load_dotenv()


@pytest.mark.usefixtures("primary_account")
@pytest.fixture(scope="session")
def sdk(primary_account):
    signer = primary_account
    sdk = Web3sdksSDK("http://localhost:8545", signer)
    return sdk
