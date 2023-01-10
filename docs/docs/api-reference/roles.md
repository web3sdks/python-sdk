# Roles

::: web3sdks.types.role

## Example Usage

```py
from web3sdks.types import Role

nft_module = sdk.get_nft_module("YOUR_NFT_MODULE_ADDRESS")
nft_module.grant_role(Role.admin, "SOME_WALLET_ADDRESS")
```