import unittest
from os import environ

from web3sdks import SdkOptions, Web3sdksSdk
from web3sdks.modules.bundle import BundleModule
from web3sdks.modules.currency import CurrencyModule
from web3sdks.modules.nft import NftModule
from web3sdks.modules.nft_types import MintArg
from web3sdks.modules.nft_v1 import NftModule as NftModuleV1

from .constants import (
    TEST_NFT_CONTRACT_ADDRESS,
    TEST_OLD_NFT_CONTRACT_ADDRESS,)


class TestRoles(unittest.TestCase):
    sdk: Web3sdksSdk
    bundle_module: BundleModule
    nft_module: NftModule
    nft_modulev1: NftModuleV1
    currency_module: CurrencyModule

    @classmethod
    def setUpClass(self):
        self.sdk = Web3sdksSdk(SdkOptions(
            private_key=environ['PKEY']
        ), "https://rpc-mumbai.maticvigil.com")
        self.nft_module = self.sdk.get_nft_module(
            TEST_NFT_CONTRACT_ADDRESS)
        self.nft_modulev1 = self.sdk.get_nft_module(
            TEST_OLD_NFT_CONTRACT_ADDRESS, True)

    def test_nft_mint_old(self):
        """
        Test that tries to instantiate the NFT module
        """
        result = self.nft_modulev1.mint(MintArg(
            name="test",
            description="test",
            image="test",
        ))
        self.assertIsNotNone(result, "The resulting nft should not be None")

    def test_nft_mint(self):
        """
        Test that tries to instantiate the NFT module
        """
        result = self.nft_module.mint(MintArg(
            name="test",
            description="test",
            image="test",
        ))
        self.assertIsNotNone(result, "The resulting nft should not be None")


if __name__ == '__main__':
    unittest.main()
