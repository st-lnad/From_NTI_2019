from web3 import Web3, HTTPProvider
import time
import argparse
import json
import sys
import face_help
import service_function
import requests
import re
from datetime import datetime

network_config=open('network.json', 'r')
rpcUrl=str(json.load(network_config)['rpcUrl'])
web3 = Web3(HTTPProvider(rpcUrl))

def key_to_value(args):
    if args.balance != " ":
        # Получение баланса
        try:
            pin_code = str(args.balance)
            # Получение ID
            f = open('person.json', 'r')

            account_config = json.load(f)
            uuid = str(account_config['id'])
            uuid = uuid.replace('-', '')
            # Генерация приватного ключа
            private_key = service_function.generate_private_key(uuid=uuid, pin_code=pin_code)
            address = service_function.generate_address(private_key)
            balance = int(service_function.getBalance(address))
            balancereal = balance
            currency = ''
            i = 0
            smen = False
            while balancereal / 10 ** i > 10.0:
                i += 3

            if (balancereal / 10 ** i) < 1.0:
                i -= 3
                smen = True
            if i == 18:
                currency = 'poa'
            if i == 15:
                currency = 'finney'
            if i == 12:
                currency = 'szabo'
            if i == 9:
                currency = 'gwei'
            if i == 6:
                currency = 'mwei'
            if i == 3:
                currency = 'kwei'
            if i == 0:
                currency = 'wei'
            if smen == True:
                balancereal = round(balancereal / 10 ** i, 6)
            else:
                balancereal = round(balancereal / 10 ** i, 6)
            if str(balancereal) == '0.0':
                balancereal = 0
                currency = 'poa'
            if str(balancereal)[len(str(balancereal)) - 1] == '0':
                balancereal = int(balancereal)

            print('Your balance is ' + str(balancereal) + ' ' + currency)
        except:
            print('ID is not found')
    elif args.find != " ":
        face_help.verlorene(str(args.find))
    elif args.add != " ":
        pin_code = str(args.add[0])
        phone_number = str(args.add[1])

        pattern = re.compile("^(\+7)\d{3}\d{7}$")
        result = pattern.search(phone_number)
        if str(result) == "None":
            '''AC-014-07(Закрыт)'''
            print("Incorrect phone number")
            sys.exit(0)
        # Генерация приватного ключа
        try:
            f = open('person.json', 'r')
            account_config = json.load(f)
            uuid = str(account_config['id'])
            uuid = uuid.replace('-', '')
            private_key = service_function.generate_private_key(uuid=uuid, pin_code=pin_code)
            address = service_function.generate_address(private_key)
            try:
                d = open('registrar.json', 'r')
                account_config = json.load(d)
                contract_address = str(account_config['registrar']['address'])
                try:
                    balance = service_function.getBalance(address)
                    Krucke = 1 / balance
                    try:
                        headers = {
                            'accept': 'application/json',
                        }
                        with open("registrar.bin") as bin_file:
                            content = json.loads(bin_file.read())
                            bytecode = content['object']
                        with open("registrar.abi") as abi_file:
                            abi = json.loads(abi_file.read())
                        contract_reg = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi,
                                                         bytecode=bytecode)
                        f = open('network.json', 'r')


                        try:
                            checkAddr=contract_reg.functions.reg_request_check(address).call()
                            time.sleep(5)
                            if checkAddr=='Full':
                                Krucke1=1/0
                            elif checkAddr=='Empty':
                                try:
                                    checkReg = contract_reg.functions.reg_account_check(address).call()
                                    if checkReg=='Full':
                                        bone3=1/0
                                    elif checkReg=='Empty':
                                        timestamp=str(time.time())
                                        tx = contract_reg.functions.reg_request(phone_number, timestamp).buildTransaction({'gas': 3000000 ,
                                                                                                    'nonce': web3.eth.getTransactionCount(
                                                                                                        web3.eth.account.privateKeyToAccount(
                                                                                                            str(private_key)).address)})
                                        signed_tx = web3.eth.account.signTransaction(tx, private_key)
                                        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                                        time.sleep(5)
                                        print('Registration request sent by '+tx_hash.hex())
                                except:
                                    pass
                        except:
                            print('Registration request already sent')
                    except:
                        print('Seems that the contract address is not the registrar contract')
                except:
                    print('No funds to send the request')
            except:
                print("No contract address")

        except:
            print('ID is not found')
        # Создание соответсвий
    elif args.delete != " ":
        pin_code = str(args.delete)
        try:
            f = open('person.json', 'r')
            account_config = json.load(f)
            uuid = str(account_config['id'])
            uuid = uuid.replace('-', '')
            private_key = service_function.generate_private_key(uuid=uuid, pin_code=pin_code)
            address = service_function.generate_address(private_key)
            try:
                d = open('registrar.json', 'r')
                account_config = json.load(d)
                contract_address = str(account_config['registrar']['address'])
                try:
                    balance = service_function.getBalance(address)
                    Krucke = 1 / balance
                    try:
                        headers = {
                            'accept': 'application/json',
                        }
                        with open("registrar.bin") as bin_file:
                            content = json.loads(bin_file.read())
                            bytecode = content['object']
                        with open("registrar.abi") as abi_file:
                            abi = json.loads(abi_file.read())
                        contract_reg = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi,
                                                         bytecode=bytecode)


                        try:
                            add_or_noadd = contract_reg.functions.get_status(address).call()
                            if add_or_noadd:
                                Krucke2=1/0
                            elif not add_or_noadd:
                                Krucke3=1/0
                            else:
                                try:
                                    checkReg = contract_reg.functions.reg_account_check(web3.toChecksumAddress(address)).call()
                                    print(checkReg)
                                    if checkReg=='Empty':
                                        bone3=1/0
                                    elif checkReg=='Full':
                                        timestamp=str(time.time())
                                        phone_number = contract_reg.functions.get_phone_from_address(address).call()
                                        tx = contract_reg.functions.unreg_request(phone_number, timestamp).buildTransaction({'gas': 3000000 ,
                                                                                                    'nonce': web3.eth.getTransactionCount(
                                                                                                        web3.eth.account.privateKeyToAccount(
                                                                                                            str(private_key)).address)})
                                        signed_tx = web3.eth.account.signTransaction(tx, private_key)
                                        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                                        time.sleep(5)
                                        print('Unregistration request sent by '+tx_hash.hex())
                                except:
                                    print('Account is not registered yet')
                        except:
                            if add_or_noadd:
                                print('Account is not registered yet')
                            elif not add_or_noadd:
                                print('Unregistration request already sent')
                    except:
                        print('Seems that the contract address is not the registrar contract')
                except:
                    print('No funds to send the request')
            except:
                print("No contract address")

        except:
            print('ID is not found')
    elif args.cancel != " ":
        pin_code = str(args.cancel)
        try:
            f = open('person.json', 'r')
            account_config = json.load(f)
            uuid = str(account_config['id'])
            uuid = uuid.replace('-', '')
            private_key = service_function.generate_private_key(uuid=uuid, pin_code=pin_code)
            address = service_function.generate_address(private_key)
            try:
                d = open('registrar.json', 'r')
                account_config = json.load(d)
                contract_address = str(account_config['registrar']['address'])
                try:
                    balance = service_function.getBalance(address)
                    Krucke = 1 / balance
                    try:
                        headers = {
                            'accept': 'application/json',
                        }
                        with open("registrar.bin") as bin_file:
                            content = json.loads(bin_file.read())
                            bytecode = content['object']
                        with open("registrar.abi") as abi_file:
                            abi = json.loads(abi_file.read())
                        contract_reg = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi,bytecode=bytecode)



                        try:
                            checkList = contract_reg.functions.reg_request_check(address).call()
                            time.sleep(5)
                            if checkList == 'Empty':
                                Krucke1 = 1 / 0
                            elif checkList == 'Full':
                                timestamp = str(time.time())
                                tx = contract_reg.functions.request_cancel(address).buildTransaction(
                                    {'gas': 3000000,
                                     'nonce': web3.eth.getTransactionCount(
                                         web3.eth.account.privateKeyToAccount(
                                             str(
                                                 private_key)).address)})
                                signed_tx = web3.eth.account.signTransaction(tx, private_key)
                                tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                                time.sleep(5)
                                print('Registration canceled by ' + tx_hash.hex())
                        except:
                            print('No requests found')
                    except:
                        print('Seems that the contract address is not the registrar contract')
                except:
                    print('No funds to send the request')
            except:
                print("No contract address")

        except:
            print('ID is not found')
    elif args.send != " ":
        # Получение данных
        pin_code = str(args.send[0])
        phone_number = str(args.send[1])
        value = int(args.send[2])

        pattern = re.compile("^(\+7)\d{3}\d{7}$")
        result = pattern.search(phone_number)
        if str(result) == "None":
            '''AC-017-05(Закрыт)'''
            print("Incorrect phone number")
            sys.exit(0)

        # Генерация приватного ключа
        f = open('person.json', 'r')
        account_config = json.load(f)
        uuid = str(account_config['id'])
        uuid = uuid.replace('-', '')
        private_key = service_function.generate_private_key(uuid=uuid, pin_code=pin_code)
        address = service_function.generate_address(private_key)
        d = open('registrar.json', 'r')
        account_config = json.load(d)
        contract_address = str(account_config['registrar']['address'])
        with open("registrar.bin") as bin_file:
            content = json.loads(bin_file.read())
            bytecode = content['object']
        with open("registrar.abi") as abi_file:
            abi = json.loads(abi_file.read())
        contract_reg = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi, bytecode=bytecode)
        address_recipient = contract_reg.functions.get_address_from_phone(str(phone_number)).call()

        if address_recipient == "0x0000000000000000000000000000000000000000":
            '''AC-017-03(Закрыт без контракта)'''
            print("No account with the phone number " + phone_number)
            sys.exit(0)
        else:
            #Создание транзакции и отправка денег
            try:
                transaction = {
                'to': web3.toChecksumAddress(address_recipient),
                'from': web3.toChecksumAddress(address),
                'value': value,
                'gas': 21000,
                'gasPrice': web3.eth.gasPrice,
                'nonce': web3.eth.getTransactionCount(address)
                }
                signed_txn = web3.eth.account.signTransaction(transaction, private_key)
                tx = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
                time.sleep(4)
            # Масштабирование
                i = 0
                smen = False
                while value / 10 ** (i) > 10.0:
                    i += 3
                if value / 10 ** i < 1.0:
                    i -= 3
                    smen = True
                if i == 18:
                    currency = 'poa'
                if i == 15:
                    currency = 'finney'
                if i == 12:
                    currency = 'szabo'
                if i == 9:
                    currency = 'gwei'
                if i == 6:
                    currency = 'mwei'
                if i == 3:
                    currency = 'kwei'
                if i == 0:
                    currency = 'wei'
                if smen:
                    value = round(value / 10 ** i, 6)
                else:
                    # test
                    value = round(value / 10 ** i, 6)

                if str(value)[len(str(value)) - 1] == '0':
                    value = int(value)
                print('Payment of ' + str(value) + ' ' + currency + ' to "' + address_recipient + '" scheduled')
                print('Transaction Hash: ' + tx.hex())
            except:
                '''AC-017-04(Закрыт)'''
                print("No funds to send the payment")
    elif args.ops != " ":
        pin_code = str(args.ops)
        # Генерация приватного ключа
        f = open('person.json', 'r')
        account_config = json.load(f)
        uuid = str(account_config['id'])
        uuid = uuid.replace('-', '')
        private_key = service_function.generate_private_key(uuid=uuid, pin_code=pin_code)
        address = service_function.generate_address(private_key)
        # print(private_key)
        # print(address)
        headers = {
            'accept': 'application/json'
        }
        param = {
            'module': 'account',
            'action': 'txlist',
            'address': address
        }
        response = requests.get('https://blockscout.com/poa/sokol/api', params=param, headers=headers)
        info = response.text
        list = json.loads(info)['result']
        for j in range(0, len(list)):

            timestamp = int(list[j]['timeStamp'])
            value = int(list[j]['value'])
            if value != 0:
                calendar = datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S %d.%m.%Y')
                i = 0
                smen = False
                while value / 10 ** i > 10.0:
                    i += 3

                if (value / 10 ** i) < 1.0:
                    i -= 3
                    smen = True
                if i == 18:
                    currency = 'poa'
                if i == 15:
                    currency = 'finney'
                if i == 12:
                    currency = 'szabo'
                if i == 9:
                    currency = 'gwei'
                if i == 6:
                    currency = 'mwei'
                if i == 3:
                    currency = 'kwei'
                if i == 0:
                    currency = 'wei'
                if smen == True:
                    value = round(value / 10 ** i, 6)
                else:
                    value = round(value / 10 ** i, 6)
                if str(value)[len(str(value)) - 1] == '0':
                    value = int(value)

                from_or_to = ''

                if address == web3.toChecksumAddress(list[j]['to']):
                    address_recipient_or_sender=Web3.toChecksumAddress(str(list[j]['from']))
                    from_or_to = 'FROM'
                    d = open('registrar.json', 'r')
                    account_config = json.load(d)
                    contract_address = str(account_config['registrar']['address'])
                    with open("registrar.bin") as bin_file:
                        content = json.loads(bin_file.read())
                        bytecode = content['object']
                    with open("registrar.abi") as abi_file:
                        abi = json.loads(abi_file.read())
                    contract_reg = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi,
                                                     bytecode=bytecode)
                    number = str(contract_reg.functions.get_phone_from_address(str(address_recipient_or_sender)).call())


                elif address == web3.toChecksumAddress(list[j]['from']):
                    address_recipient_or_sender = web3.toChecksumAddress(str(list[j]['to']))
                    d = open('registrar.json', 'r')
                    account_config = json.load(d)
                    contract_address = str(account_config['registrar']['address'])
                    with open("registrar.bin") as bin_file:
                        content = json.loads(bin_file.read())
                        bytecode = content['object']
                    with open("registrar.abi") as abi_file:
                        abi = json.loads(abi_file.read())
                    contract_reg = web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi,
                                                     bytecode=bytecode)
                    number = str(contract_reg.functions.get_phone_from_address(str(address_recipient_or_sender)).call())
                    from_or_to = "TO"

                # Контракт
                if number != '':
                    timestamp_info = float(contract_reg.functions.get_timestamp_from_address(str(address_recipient_or_sender)).call())
                    if float(timestamp) > timestamp_info:
                        print(calendar + " " + from_or_to + " " + number + " " + str(value) + " " + currency)


parser = argparse.ArgumentParser()
parser.add_argument('--balance', default=" ", nargs='?')
parser.add_argument('--find', default=" ", nargs='?')
parser.add_argument('--actions', default="zero", nargs='?')
parser.add_argument('--add', default=" ", nargs='+')
parser.add_argument('--delete', '-d', default=" ", nargs='?')
parser.add_argument('--cancel', default=" ", nargs='?')
parser.add_argument('--send', default=" ", nargs='+')
parser.add_argument('--receive', default=" ", nargs='+')
parser.add_argument('--withdraw', default=" ", nargs='+')
parser.add_argument('--ops', default=" ", nargs='?')
parser.add_argument('--opsall', default=" ", nargs='+')
parser.set_defaults(func=key_to_value)
if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
