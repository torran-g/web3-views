# Web3 Views
A library that provides a simple convenience interface for reading data from Smart Contracts.

## Usage
Smart Contract's

```python
In [1]: import json
   ...: import types
   ...: from pathlib import Path
   ...: from web3 import Web3
   ...: from src.config import settings
   ...: from src.sc_wrapper import view
   ...:
   ...: # Standard Web3.py setup
   ...: w3 = Web3(Web3.HTTPProvider(settings.rpc_endpoint))
   ...: contract_abi = json.loads(Path(settings.contract_abi_path).read_text())
   ...: contract = w3.eth.contract(address=settings.contract_address, abi=contract_abi)
   ...:
   ...: # Create the contract view object, this example uses the Compound Finance (https://compound.finance/) contract
   ...: contract_view = view(contract)

In [2]: contract_view.name
Out[2]: 'Compound USDC'

In [3]: contract_view(block_identifier="finalized").decimals
Out[3]: 6

In [4]: contract_view.get_supply_rate(contract_view.utilization)
Out[4]: 1698139133

In [5]: dict(contract_view)
Out[5]:
{'base_accrual_scale': 1000000,
 'base_borrow_min': 100000000,
 'base_index_scale': 1000000000000000,
 'base_min_for_rewards': 1000000000000,
 'base_scale': 1000000,
 'base_token': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
 'base_token_price_feed': '0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6',
 'base_tracking_borrow_speed': 4414467592592,
 'base_tracking_supply_speed': 2979166666666,
 'borrow_kink': 930000000000000000,
 'borrow_per_second_interest_rate_base': 317097919,
 'borrow_per_second_interest_rate_slope_high': 47564687975,
 'borrow_per_second_interest_rate_slope_low': 1055936073,
 'decimals': 6,
 ...
 ```
