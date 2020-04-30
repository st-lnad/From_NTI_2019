from web3 import Web3, HTTPProvider
import json
import requests

network_config=open('network.json', 'r')
rpcUrl=str(json.load(network_config)['rpcUrl'])
web3 = Web3(HTTPProvider(rpcUrl))


def get_gas():
    network_config_test = open('network.json', 'r')
    defaultGasPrice = str(json.load(network_config_test)['defaultGasPrice'])
    return defaultGasPrice


def get_gasprice():
    try:
        headers = {
            'accept': 'application/json',
        }
        network_config_test = open('network.json', 'r')
        site=str(json.load(network_config_test)['gasPriceUrl'])
        response = requests.get(site, headers=headers)
        fast = int(json.loads(response.text)['fast'] * 1000000000)
        return fast
    except:
        #print('Except')
        network_config_test = open('network.json', 'r')
        fast = str(json.load(network_config_test)['defaultGasPrice'])
        return fast

def generate_private_key(uuid, pin_code):
    privateKey = web3.keccak(web3.keccak(web3.keccak(web3.keccak(
        web3.keccak(text='') + int(uuid, 16).to_bytes(16, 'big') + int(pin_code[0], 16).to_bytes(1,
                                                                                                 'big')) + int(
        uuid, 16).to_bytes(16, 'big') + int(pin_code[1], 16).to_bytes(1, 'big')) + int(uuid, 16).to_bytes(
        16,
        'big') + int(
        pin_code[2], 16).to_bytes(1, 'big')) + int(uuid, 16).to_bytes(16, 'big') + int(pin_code[3],
                                                                                       16).to_bytes(1,
                                                                                                    'big')).hex()
    return privateKey


def generate_address(private_key):
    addrlast = web3.eth.account.privateKeyToAccount(private_key).address
    return addrlast


def getBalance(addr):
    balance = web3.eth.getBalance(Web3.toChecksumAddress(addr))
    return balance
