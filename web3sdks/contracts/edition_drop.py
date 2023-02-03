from typing import Final, List, Optional

from web3 import Web3
from web3sdks.abi import DropERC1155
from web3sdks.abi.drop_erc721 import IDropAllowlistProof
from web3sdks.common.claim_conditions import prepare_claim
from web3sdks.constants.role import Role
from web3sdks.core.classes.contract_events import ContractEvents
from web3sdks.core.classes.contract_metadata import ContractMetadata
from web3sdks.core.classes.contract_platform_fee import ContractPlatformFee
from web3sdks.core.classes.contract_roles import ContractRoles
from web3sdks.core.classes.contract_royalty import ContractRoyalty
from web3sdks.core.classes.contract_sales import ContractPrimarySale
from web3sdks.core.classes.contract_wrapper import ContractWrapper
from web3sdks.core.classes.erc_1155 import ERC1155
from web3sdks.core.classes.ipfs_storage import IpfsStorage
from web3sdks.types.contract import ContractType
from web3sdks.types.contracts.claim_conditions import ClaimVerification
from web3sdks.types.nft import NFTMetadata, NFTMetadataInput
from web3sdks.types.sdk import SDKOptions
from web3sdks.types.settings.metadata import EditionDropContractMetadata
from eth_account.account import LocalAccount
from web3sdks.core.classes.drop_erc1155_claim_conditions import (
    DropERC1155ClaimConditions,
)
from zero_ex.contract_wrappers.tx_params import TxParams
from web3sdks.types.tx import TxResultWithId
from web3.eth import TxReceipt


class EditionDrop(ERC1155[DropERC1155]):
    """
    Setup a collection of NFTs with a customizable number of each NFT that are minted as users claim them.

    ```python
    from web3sdks import Web3sdksSDK

    # You can customize this to a supported network or your own RPC URL
    network = "mumbai"

    # Now we can create a new instance of the SDK
    sdk = Web3sdksSDK(network)

    # If you want to send transactions, you can instantiate the SDK with a private key instead:
    #   sdk = Web3sdksSDK.from_private_key(PRIVATE_KEY, network)

    contract = sdk.get_edition_drop("{{contract_address}}")
    ```
    """

    _abi_type = DropERC1155

    contract_type: Final[ContractType] = ContractType.EDITION_DROP
    contract_roles: Final[List[Role]] = [Role.ADMIN, Role.MINTER, Role.TRANSFER]

    metadata: ContractMetadata[DropERC1155, EditionDropContractMetadata]
    roles: ContractRoles
    primary_sale: ContractPrimarySale[DropERC1155]
    platform_fee: ContractPlatformFee[DropERC1155]
    royalty: ContractRoyalty[DropERC1155]
    claim_conditions: DropERC1155ClaimConditions
    events: ContractEvents[DropERC1155]

    def __init__(
        self,
        provider: Web3,
        address: str,
        storage: IpfsStorage,
        signer: Optional[LocalAccount] = None,
        options: SDKOptions = SDKOptions(),
    ):
        abi = DropERC1155(provider, address)
        contract_wrapper = ContractWrapper(abi, provider, signer, options)
        super().__init__(contract_wrapper, storage)

        self.metadata = ContractMetadata(
            contract_wrapper, storage, EditionDropContractMetadata
        )
        self.roles = ContractRoles(contract_wrapper, self.contract_roles)
        self.primary_sale = ContractPrimarySale(contract_wrapper)
        self.platform_fee = ContractPlatformFee(contract_wrapper)
        self.royalty = ContractRoyalty(contract_wrapper, self.metadata)
        self.claim_conditions = DropERC1155ClaimConditions(
            self._contract_wrapper, self.metadata, self._storage
        )
        self.events = ContractEvents(contract_wrapper)

    def create_batch(
        self, metadatas: List[NFTMetadataInput]
    ) -> List[TxResultWithId[NFTMetadata]]:
        """
        Create a batch of NFTs.

        ```python
        from web3sdks.types.nft import NFTMetadataInput, EditionMetadataInput

        # Note that you can customize this metadata however you like
        metadatas_with_supply = [
            EditionMetadataInput(
                NFTMetadataInput.from_json({
                    "name": "Cool NFT",
                    "description": "This is a cool NFT",
                    "image": open("path/to/file.jpg", "rb"),
                }),
                100
            ),
            EditionMetadataInput(
                NFTMetadataInput.from_json({
                    "name": "Cooler NFT",
                    "description": "This is a cooler NFT",
                    "image": open("path/to/file.jpg", "rb"),
                }),
                100
            )
        ]

        txs = contract.create_batch(metadata_with_supply)
        first_token_id = txs[0].id
        first_nft = txs[0].data()
        ```

        :param metadatas: List of NFT metadata inputs.
        :return: List of tx results with ids for created NFTs.
        """

        start_file_number = (
            self._contract_wrapper._contract_abi.next_token_id_to_mint.call()
        )
        batch = self._storage.upload_metadata_batch(
            [metadata.to_json() for metadata in metadatas],
            start_file_number,
            self._contract_wrapper._contract_abi.contract_address,
            self._contract_wrapper.get_signer_address(),
        )
        base_uri = batch.base_uri

        receipt = self._contract_wrapper.send_transaction(
            "lazy_mint",
            [
                len(batch.metadata_uris),
                base_uri if base_uri.endswith("/") else base_uri + "/",
                Web3.toBytes(text=""),
            ],
        )

        events = self._contract_wrapper.get_events("TokensLazyMinted", receipt)
        start_index = events[0].get("args").get("startTokenId")  # type: ignore
        ending_index = events[0].get("args").get("endTokenId")  # type: ignore
        results = []

        for id in range(start_index, ending_index + 1):
            results.append(
                TxResultWithId(
                    receipt,
                    id=id,
                    data=lambda: self._get_token_metadata(id),
                )
            )

        return results

    def claim_to(
        self,
        destination_address: str,
        token_id: int,
        quantity: int,
    ) -> TxReceipt:
        """
        Claim NFTs to a destination address.

        ```python
        address = {{wallet_address}}
        token_id = 0
        quantity = 1

        tx = contract.claim_to(address, token_id, quantity)
        receipt = tx.receipt
        claimed_token_id = tx.id
        claimed_nft = tx.data()
        ```

        :param destination_address: Destination address to claim to.
        :param token_id: token ID of the token to claim.
        :param quantity: Number of NFTs to claim.
        :param proofs: List of merkle proofs.
        :return: tx receipt of the claim
        """

        claim_verification = self._prepare_claim(token_id, quantity)
        overrides: TxParams = TxParams(value=claim_verification.value)

        proof = IDropAllowlistProof(
            proof=claim_verification.proofs,
            quantityLimitPerWallet=claim_verification.max_claimable,
            pricePerToken=claim_verification.price_in_proof,
            currency=claim_verification.currency_address_in_proof
        )

        return self._contract_wrapper.send_transaction(
            "claim",
            [
                destination_address,
                token_id,
                quantity,
                claim_verification.currency_address,
                claim_verification.price,
                proof,
                "",
            ],
            overrides
        )

    def claim(
        self,
        token_id: int,
        quantity: int,
    ) -> TxReceipt:
        """
        Claim NFTs.

        :param quantity: Number of NFTs to claim.
        :param token_id: token ID of the token to claim.
        :param proofs: List of merkle proofs.
        :return: tx receipt of the claim
        """
        return self.claim_to(
            self._contract_wrapper.get_signer_address(),
            token_id,
            quantity,
        )

    """
    INTERNAL FUNCTIONS
    """

    def _prepare_claim(
        self,
        token_id: int,
        quantity: int,
    ) -> ClaimVerification:
        address_to_claim = self._contract_wrapper.get_signer_address()
        active = self.claim_conditions.get_active(token_id)
        merkle_metadata = self.metadata.get().merkle

        return prepare_claim(
            address_to_claim,
            quantity,
            active,
            merkle_metadata,
            self._contract_wrapper,
            self._storage,
        )
