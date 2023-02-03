<a id="core.classes.erc_20"></a>

# core.classes.erc\_20

<a id="core.classes.erc_20.ERC20"></a>

## ERC20 Objects

```python
class ERC20(BaseContract[TokenERC20])
```

<a id="core.classes.erc_20.ERC20.get"></a>

#### get

```python
def get() -> Currency
```

Get the token metadata including name, symbol, decimals, etc.

```python
token = contract.get()
print(token)
```

**Returns**:

token metadata

<a id="core.classes.erc_20.ERC20.balance"></a>

#### balance

```python
def balance() -> CurrencyValue
```

Get the token balance of the connected wallet.

```python
balance = contract.balance()
print(balance)
```

**Returns**:

balance of the connected wallet

<a id="core.classes.erc_20.ERC20.balance_of"></a>

#### balance\_of

```python
def balance_of(address: str) -> CurrencyValue
```

Get the balance of the specified wallet

```python
address = "{{wallet_address}}"
balance = contract.balance_of(address)
print(balance)
```

**Arguments**:

- `address`: wallet address to check the balance of

**Returns**:

balance of the specified wallet

<a id="core.classes.erc_20.ERC20.total_supply"></a>

#### total\_supply

```python
def total_supply() -> CurrencyValue
```

Get the total minted supply of the token.

**Returns**:

total minted supply of the token

<a id="core.classes.erc_20.ERC20.allowance"></a>

#### allowance

```python
def allowance(spender: str) -> CurrencyValue
```

Get a specific spenders allowance of this token for the connected wallet.

```python
spender = "{{wallet_address}}"
allowance = contract.allowance(spender)
```

**Arguments**:

- `spender`: wallet address to check the allowance of

**Returns**:

allowance of the connected wallet

<a id="core.classes.erc_20.ERC20.allowance_of"></a>

#### allowance\_of

```python
def allowance_of(owner: str, spender: str) -> CurrencyValue
```

Get the allowance of the specified spender for a specified owner.

```python
# Address of the wallet who owns the funds
address = "{{wallet_address}}"

# Address of the wallet to check the token allowance
spender = "0x..."

allowance = contract.allowance_of(address, spender)
print(allowance)
```

**Arguments**:

- `owner`: wallet address whose assets will be spent
- `spender`: wallet address to check the allowance of

**Returns**:

allowance of the specified spender for the specified owner

<a id="core.classes.erc_20.ERC20.is_transfer_restricted"></a>

#### is\_transfer\_restricted

```python
def is_transfer_restricted() -> bool
```

Check whether transfer is restricted for tokens in this module.

**Returns**:

True if transfer is restricted, False otherwise

<a id="core.classes.erc_20.ERC20.transfer"></a>

#### transfer

```python
def transfer(to: str, amount: Price) -> TxReceipt
```

Transfer a specified amount of tokens from the connected wallet to a specified address.

```python
# Address to send tokens to
to = "0x...

# Amount of tokens to transfer
amount = 0.1

contract.transfer(to, amount)
```

**Arguments**:

- `to`: wallet address to transfer the tokens to
- `amount`: amount of tokens to transfer

**Returns**:

transaction receipt of the transfer

<a id="core.classes.erc_20.ERC20.transfer_from"></a>

#### transfer\_from

```python
def transfer_from(fr: str, to: str, amount: Price) -> TxReceipt
```

Transfer a specified amount of tokens from one specified address to another.

```python
# Address to send tokens from
fr = "{{wallet_address}}"

# Address to send tokens to
to = "0x..."

# Amount of tokens to transfer
amount = 0.1

contract.transfer_from(fr, to, amount)
```

**Arguments**:

- `fr`: wallet address to transfer the tokens from
- `to`: wallet address to transfer the tokens to
- `amount`: amount of tokens to transfer

**Returns**:

transaction receipt of the transfer

<a id="core.classes.erc_20.ERC20.set_allowance"></a>

#### set\_allowance

```python
def set_allowance(spender: str, amount: Price) -> TxReceipt
```

Sets the allowance of the specified wallet over the connected wallets funds to

a specified amount.

```python
spender = "0x..."
amount = 100
contract.set_allowance(spender, amount)
```

**Arguments**:

- `spender`: wallet address to set the allowance of
- `amount`: amount to set the allowance to

**Returns**:

transaction receipt of the allowance set

<a id="core.classes.erc_20.ERC20.transfer_batch"></a>

#### transfer\_batch

```python
def transfer_batch(args: List[TokenAmount])
```

Transfer tokens from the connected wallet to many wallets.

```python
from web3sdks.types.currency import TokenAmount

data = [
    TokenAmount("{{wallet_address}}", 0.1),
    TokenAmount("0x...", 0.2),
]

contract.transfer_batch(data)
```

**Arguments**:

- `args`: list of token amounts and addressed to transfer to

**Returns**:

transaction receipt of the transfers

<a id="core.classes.erc_20.ERC20.burn"></a>

#### burn

```python
def burn(amount: Price) -> TxReceipt
```

Burn a specified amount of tokens from the connected wallet.

```python
amount = 0.1
contract.burn(amount)
```

**Arguments**:

- `amount`: amount of tokens to burn

**Returns**:

transaction receipt of the burn

<a id="core.classes.erc_20.ERC20.burn_from"></a>

#### burn\_from

```python
def burn_from(holder: str, amount: Price) -> TxReceipt
```

Burn a specified amount of tokens from a specified wallet.

```python
holder = "{{wallet_address}}"
amount = 0.1
contract.burn_from(holder, amount)
```

**Arguments**:

- `holder`: wallet address to burn the tokens from
- `amount`: amount of tokens to burn

**Returns**:

transaction receipt of the burn

