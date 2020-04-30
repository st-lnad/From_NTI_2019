import argparse
import json
import sys
import requests
import time
from web3 import Web3, HTTPProvider
web3 = Web3(HTTPProvider('https://sokol.poa.network'))
import service_function

def key_to_value(args):
    if args.list=="add":
        print("Add")
    if args.list=="del":
        print("Del")
    if args.confirm != " ":
        pin_code=args.confirm
        c = open('person.json', 'r')
        account_config = json.load(c)
        uuid = str(account_config['id'])
        uuid = uuid.replace('-', '')
        private_key = service_function.generate_private_key(uuid=uuid, pin_code=pin_code)
        address_for_confirm = web3.eth.account.privateKeyToAccount(private_key).address
        #print(address_for_confirm)
        try:
            d = open('registrar.json', 'r')
            contract_config = json.load(d)
            contract_address = str(contract_config['registrar']['address'])
            try:
                f = open('network.json', 'r')
                private_key = str(json.load(f)['privKey'])
                private_key_for_senders_account = private_key
                try:
                    address = Web3.toChecksumAddress(
                        web3.eth.account.privateKeyToAccount('0x' + str(private_key_for_senders_account)).address)

                    with open("registrar.bin") as bin_file:
                        content = json.loads(bin_file.read())
                        bytecode = content['object']

                    with open("registrar.abi") as abi_file:
                        abi = json.loads(abi_file.read())

                    #print(contract_address)

                    contract_reg = web3.eth.contract(address=contract_address, abi=abi,
                                                     bytecode=bytecode)

                    try:
                        own = str(contract_reg.functions.get_owner().call())
                        #print(own)
                        #print(address)
                        if own.__eq__(address):
                            if (contract_reg.functions.reg_request_check(address_for_confirm).call()=='Full'):
                                add_or_noadd=contract_reg.functions.get_status(address_for_confirm).call()
                                #print(add_or_noadd)
                                if  add_or_noadd:
                                    #print('Nice')
                                    phone_number=contract_reg.functions.get_number_from_request(address_for_confirm).call()
                                    #print('Phone number:',phone_number)
                                    timestamp=str(time.time())
                                    fast = int(service_function.get_gasprice())
                                    tx=contract_reg.functions.reg_forward(address_for_confirm, str(phone_number),timestamp).buildTransaction({'gasPrice': fast, 'nonce': web3.eth.getTransactionCount(web3.eth.account.privateKeyToAccount('0x' + str(private_key_for_senders_account)).address)})
                                    signed_tx = web3.eth.account.signTransaction(tx, private_key_for_senders_account)
                                    tx_hash_confirm = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                                    time.sleep(5)
                                    #print('Very nice')
                                    timestamp = str(time.time())
                                    tx = contract_reg.functions.request_cancel(address_for_confirm).buildTransaction(
                                            {'gas': 3000000,
                                             'nonce': web3.eth.getTransactionCount(
                                                 web3.eth.account.privateKeyToAccount('0x'+
                                                     str( private_key_for_senders_account)).address)})
                                    signed_tx = web3.eth.account.signTransaction(tx, private_key_for_senders_account)
                                    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                                    time.sleep(5)
                                    #print('Did')
                                    print('Confirmed by '+tx_hash_confirm.hex())
                                elif not add_or_noadd:

                                    phone_number = contract_reg.functions.get_phone_from_address(address_for_confirm).call()
                                    #print(phone_number)
                                    timestamp = str(time.time())
                                    fast = int(service_function.get_gasprice())

                                    tx=contract_reg.functions.unreg_forward(address_for_confirm).buildTransaction({'gasPrice': fast, 'nonce': web3.eth.getTransactionCount(web3.eth.account.privateKeyToAccount('0x' + str(private_key_for_senders_account)).address)})
                                    #print('Nice')
                                    signed_tx = web3.eth.account.signTransaction(tx, private_key_for_senders_account)
                                    tx_hash_confirm = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                                    timestamp = str(time.time())

                                    tx = contract_reg.functions.request_cancel(address_for_confirm).buildTransaction(
                                        {'gas': 3000000,
                                         'nonce': web3.eth.getTransactionCount(
                                             web3.eth.account.privateKeyToAccount(
                                                 str(
                                                     private_key)).address)})
                                    signed_tx = web3.eth.account.signTransaction(tx, private_key_for_senders_account)
                                    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                                    time.sleep(5)
                                    print('Confirmed by ' + tx_hash_confirm.hex())
                            else:
                                transaction = {
                                    'to': web3.toChecksumAddress(address),
                                    'from': web3.toChecksumAddress(address),
                                    'value': 0,
                                    'gas': 21000,
                                    'gasPrice': web3.eth.gasPrice,
                                    'nonce': web3.eth.getTransactionCount(address)
                                }
                                signed_txn = web3.eth.account.signTransaction(transaction, private_key)
                                tx = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                                print('Failed but included in' + tx.hex())
                        else:
                            transaction = {
                            'to': web3.toChecksumAddress(address),
                            'from': web3.toChecksumAddress(address),
                            'value': 0,
                            'gas': 21000,
                            'gasPrice': web3.eth.gasPrice,
                            'nonce': web3.eth.getTransactionCount(address)
                             }
                            signed_txn = web3.eth.account.signTransaction(transaction, private_key)
                            tx = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                            print('Failed but included in' + tx.hex())

                            bone1=1/0

                    except:
                        pass

                except:
                    print('Seems that the contract address is not the registrar contract')
            except:
                print('No admin account found')
        except:
            print("No contract address")


    if args.get != " ":
        phone_number=args.get
        try:
            d = open('registrar.json', 'r')
            account_config = json.load(d)
            contract_address = str(account_config['registrar']['address'])
            with open("registrar.bin") as bin_file:
                content = json.loads(bin_file.read())
                bytecode = content['object']
            with open("registrar.abi") as abi_file:
                abi = json.loads(abi_file.read())
            contract_reg = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi, bytecode=bytecode)
            try:
                address_recipient = contract_reg.functions.get_address_from_phone(phone_number).call()
                #print(address_recipient)
                if address_recipient == "0x0000000000000000000000000000000000000000":
                    '''AC-017-03(Закрыт без контракта)'''
                    bone=1/0
                else:
                    print('Registered correspondence: '+ address_recipient)
            except:
                print('Correspondence not found')
        except:
            print('No contract address')

parser=argparse.ArgumentParser()
parser.add_argument('--list', default=" ", nargs='?')
parser.add_argument('--confirm',default=" ",nargs='?')
parser.add_argument('--get',default=" ",nargs='?')
parser.set_defaults(func=key_to_value)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)