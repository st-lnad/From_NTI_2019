import argparse
from web3 import Web3, HTTPProvider
import json
import time
import requests
import service_function


network_config=open('network.json', 'r')
rpcUrl=str(json.load(network_config)['rpcUrl'])

web3 = Web3(HTTPProvider(rpcUrl))



'''class Info(object):
    def __init__(self, file_account):
        f = open(file_account, 'r')
        account_config = json.load(f)['privKey']
        self.private_key = account_config'''


def key_to_value(args):
    if (args.deploy != " ") and (args.owner == ' ') and (args.chown == ' '):

        f = open('network.json', 'r')
        private_key = str(json.load(f)['privKey'])
        private_key_for_senders_account = private_key
        addressUser = Web3.toChecksumAddress(
            web3.eth.account.privateKeyToAccount('0x' + str(private_key_for_senders_account)).address)

        with open("registrar.bin") as bin_file:
            content = json.loads(bin_file.read())
            bytecode = content['object']

        with open("registrar.abi") as abi_file:
            abi = json.loads(abi_file.read())

        with open("payments.bin") as bin_file:
            content1 = json.loads(bin_file.read())
            bytecode_pay = content1['object']

        with open("payments.abi") as abi_file:
            abi_pay = json.loads(abi_file.read())



        Contract = web3.eth.contract(abi=abi, bytecode=bytecode)

        fastgasPrice = int(service_function.get_gasprice())
        defaultGasPrice=int(service_function.get_gas())
        if defaultGasPrice >= fastgasPrice:
            gasPrice=defaultGasPrice
        else:
            gasPrice=fastgasPrice

        tx = Contract.constructor().buildTransaction({
            'from': addressUser,
            'nonce': web3.eth.getTransactionCount(addressUser),
            'gasPrice': gasPrice,
            'gas': 1303052
        })

        signed_tx = web3.eth.account.signTransaction(tx, private_key_for_senders_account)
        txId = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        txReceipt = wait_tx_receipt(txId)
        txReceipt1=web3.eth.waitForTransactionReceipt(txId)


        Contract_pay = web3.eth.contract(abi=abi_pay, bytecode=bytecode_pay)

        fastgasPrice = int(service_function.get_gasprice())
        defaultGasPrice = int(service_function.get_gas())
        if defaultGasPrice >= fastgasPrice:
            gasPrice = defaultGasPrice
        else:
            gasPrice = fastgasPrice

        tx_pay = Contract_pay.constructor().buildTransaction({
            'from': addressUser,
            'nonce': web3.eth.getTransactionCount(addressUser),
            'gasPrice': gasPrice,
            'gas': 992814,
        })

        signed_tx_pay = web3.eth.account.signTransaction(tx_pay, private_key_for_senders_account)
        txId_pay = web3.eth.sendRawTransaction(signed_tx_pay.rawTransaction)
        txReceipt_pay = wait_tx_receipt(txId_pay)
        txReceipt_pay1=web3.eth.waitForTransactionReceipt(txId_pay)
        #print(txReceipt_pay1)


        #print(txReceipt1)







        if txReceipt_pay['status'] == 1 and txReceipt['status'] == 1:
            print("KYC Registrar: " + txReceipt['contractAddress'])
            print("Payment Handler: " + txReceipt_pay['contractAddress'])
            with open('registrar.json', 'w') as filewrite:
                data = {"registrar": {"address": Web3.toChecksumAddress(str(txReceipt1['contractAddress'])),
                                      "startBlock": int(txReceipt1['blockNumber'])},
                        "payments": {"address": Web3.toChecksumAddress(str(txReceipt_pay1['contractAddress'])),
                                     "startBlock": int(txReceipt_pay1['blockNumber'])}}
                json.dump(data, filewrite)

    ###US-00s - НАДО ДОДЕЛАТЬ ДЕПЛОЙ, БЛЭТ
    elif (args.deploy == " ") and (args.owner != " ") and (args.chown == " "):
        if (args.owner == "registrar"):
            with open("registrar.bin") as bin_file:
                content = json.loads(bin_file.read())
                bytecode = content['object']
            with open("registrar.abi") as abi_file:
                abi = json.loads(abi_file.read())
            f = open('registrar.json', 'r')
            adr = str(json.load(f)['registrar']['address'])

            contract_reg = web3.eth.contract(address=Web3.toChecksumAddress(adr), abi=abi)
            own = contract_reg.functions.get_owner().call()
            print("Admin account: " + own)
    ###
    elif (args.deploy == " ") and (args.owner == " ") and (args.chown != " "):
        '0x5F295A1d88bD80286639728dDAFb8fF9D2521626'
        '0xbfDeDB58Fd0749CF8a2896762F312770242ffe38'

        if (args.chown[0] == "registrar"):
            with open("registrar.bin") as bin_file:
                content = json.loads(bin_file.read())
                bytecode = content['object']
            with open("registrar.abi") as abi_file:
                abi = json.loads(abi_file.read())
            f = open('registrar.json', 'r')
            adr = str(json.load(f)['registrar']['address'])
            contract_reg = web3.eth.contract(address=Web3.toChecksumAddress(adr), abi=abi, bytecode=bytecode)
            f = open('network.json', 'r')
            fast = int(service_function.get_gasprice())
            private_key_for_senders_account=json.load(f)['privKey']

            tx = contract_reg.functions.set_owner(args.chown[1]).buildTransaction({'gasPrice': fast, 'nonce': web3.eth.getTransactionCount(web3.eth.account.privateKeyToAccount('0x' + str(private_key_for_senders_account)).address)})
            signed_tx = web3.eth.account.signTransaction(tx, private_key_for_senders_account)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            time.sleep(0.5)
            tx_Receipt=web3.eth.waitForTransactionReceipt(tx_hash)
            print('New admin account: '+ str(contract_reg.functions.get_owner().call()))


'''tx_hash = greeter.functions.setGreeting('Nihao').transact()

# Wait for transaction to be mined...
w3.eth.waitForTransactionReceipt(tx_hash)'''


def wait_tx_receipt(tx_hash, sleep_interval=0.5):
    while True:
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        #print(tx_receipt)
        if tx_receipt:
            return tx_receipt
        time.sleep(sleep_interval)


parser = argparse.ArgumentParser()

parser.add_argument('--deploy', default=' ', nargs='?')
parser.add_argument('--owner', default=' ', nargs='?')
parser.add_argument('--chown', default=' ', nargs='+')
parser.set_defaults(func=key_to_value)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)