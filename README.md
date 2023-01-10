# Web3sdks Python SDK

PyPi package found [here](https://pypi.org/project/web3sdks-sdk).

## Deprecation Notices

> 1 of 2
>
> The `nftlabs-sdk` pypi package will be deprecated on November 30th, 2021
>
> Please make sure you install the new `web3sdks-sdk` package found [here](https://pypi.org/project/web3sdks-sdk)
>
> In your code, update all imports to use the `web3sdks` package and switch to using the `Web3sdksSdk` package (instead of the `NftlabsSdk` package)


---

> 2 of 2
>
> The `collection` module has been renamed to `bundle` and will be deprecated on November 30th, 2021
>
> All references to `collection` module and its associated classes should be updated to `bundle` and its newely created classes.
> 
> You can find the detailed documentation for the `bundle` module [here](https://python-docs.web3sdks.com/modules.bundle.html)


### Docs
https://docs.web3sdks.com

### API Reference
https://python-docs.web3sdks.com/



## Installing the SDK

```bash
$ pip install web3sdks-sdk
```



## Package Structure

```
thidweb
├── abi       // contains autogenerated ABI contract wrappers 
├── errors    // commonly thrown errors
├── modules   // NFT, Currency, Marketplace, Pack, Bundle, etc modules
├── options   // Options classes used throughout the SDK
├── sdk.py    // NftlabsSdk class, wrapper for the entire package
├── storage   // Distributed file storage helper classes
└── types     // Types consumed by some of the methods exposed in the modules
```

## Calling the modules

You can call the NFTLabs modules by instantiating an SDK object and fetching the module with your contract address
like this:

```python
import os
from nftlabs import NftlabsSdk, SdkOptions

sdk = NftlabsSdk(SdkOptions(), "https://rpc-mumbai.maticvigil.com") # polygon testnet as an example

# Assumes your private key is assigned to the `PKEY` environment variable
sdk.set_private_key(os.getenv("PKEY"))

# Put your NFT contract address here if you want to mint your own NFTs!
nft_module = sdk.get_nft_module("0xbDfF8fb43688fB4D2184DF8029A7238ac1413A24")
print(nft_module.total_supply())
```

## Development

### Generating ABI wrappers

The `abi` package contains autogenerated code compiled by the
0xchain `abi-gen` tool found [here](https://www.npmjs.com/package/@0x/abi-gen).

Our protocols are developer at [this repo](https://github.com/nftlabs/nftlabs-protocols).

Install the `abi-gen` cli tool and use it to compile abi wrappers like this:

```bash
$ # assumes you have the nftlabs-protocols repo cloned in the parent directory
$ abi-gen --language Python -o web3sdks/abi --abis ../nftlabs-protocols/abi/NFT.json
```

Anytime there are ABI contract changes, you should regenerate the abi wrappers.


### Writing Documentation

This package uses [`PyDoctor`](https://github.com/twisted/pydoctor) to auto-generate docs. Each method, class and variable should have a detailed description of what it is meant for as a comment enclosed in triple quoation marks (`""" """`) just below the line they are defined.

Example:

Do:
```python
def my_method(self, arg1, arg2):
    """
    This part goes into the documentation.
    """
    return arg1 + arg2
```

Don't:
```python
"""
This part will not go into the documentation.
"""

def my_method(self, arg1, arg2):
    return arg1 + arg2
```


Addtionally, each module should also have a docstring at the top of the file. This will be used as a breif descroption of the module on the [homepage of the documentation](https://python-docs.web3sdks.com/). 

Example:
```python
1 """Interact with the NFT module of the app""" # docstring
2 # Module code starts from here
3 # ...
```
