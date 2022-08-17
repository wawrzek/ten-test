from solcx import compile_source
from pysys.constants import *
from ethsys.utils.solidity import Solidity


class Storage:
    GAS = 720000

    def __init__(self, test, web3, initial):
        """Create an instance of the storage contract, compile and construct a web3 instance."""
        self.test = test
        self.web3 = web3
        self.initial = initial
        self.bytecode = None
        self.abi = None
        self.contract = None
        self.contract = None
        self.contract_address = None
        self.account = None
        self.construct()

    def construct(self):
        """Compile and construct an instance. """
        file = os.path.join(PROJECT.root, 'utils', 'contracts', 'storage', 'Storage.sol')
        with open(file, 'r') as fp:
            compiled_sol = compile_source(source=fp.read(), output_values=['abi', 'bin'], solc_binary=Solidity.get_compiler())
            contract_id, contract_interface = compiled_sol.popitem()
            self.bytecode = contract_interface['bin']
            self.abi = contract_interface['abi']

        self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode).constructor(self.initial)

    def deploy(self, network, account):
        """Deploy the contract using a given account."""
        self.account = account
        tx_receipt = network.transact(self.test, self.web3, self.contract, account, self.GAS)
        self.contract_address = tx_receipt.contractAddress
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)