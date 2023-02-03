import pytest
from web3sdks.constants.currency import ZERO_ADDRESS
from web3sdks.constants.role import Role
from web3sdks.contracts.nft_drop import NFTDrop

from web3sdks.core.sdk import Web3sdksSDK
from web3sdks.types.nft import NFTMetadataInput
from web3sdks.types.settings.metadata import NFTDropContractMetadata


@pytest.mark.usefixtures("sdk", "primary_account")
@pytest.fixture(scope="function")
def nft_drop(sdk: Web3sdksSDK, primary_account) -> NFTDrop:
    sdk.update_signer(primary_account)
    nft_drop = sdk.get_nft_drop(
        sdk.deployer.deploy_nft_drop(
            NFTDropContractMetadata(
                name="SDK NFT Drop",
                primary_sale_recipient=sdk.get_signer().address,  # type: ignore
                seller_fee_basis_points=500,
                fee_recipient=ZERO_ADDRESS,
                platform_fee_basis_points=10,
                platform_fee_recipient=ZERO_ADDRESS,
            )
        )
    )
    nft_drop.roles.grant(Role.MINTER, sdk.get_signer().address)  # type: ignore
    return nft_drop


def test_create_batch(nft_drop: NFTDrop):
    metadatas = []
    for i in range(10):
        metadatas.append(NFTMetadataInput(name=f"NFT {i}"))

    nft_drop.create_batch(metadatas)
    nfts = nft_drop.get_all()

    assert len(nfts) == 10

    for i, nft in enumerate(nfts):
        assert nft.metadata.name == f"NFT {i}"

    assert nft_drop.get_total_count() == 10
    assert len(nft_drop.get_all_claimed()) == 0
    assert len(nft_drop.get_all_unclaimed()) == 10

