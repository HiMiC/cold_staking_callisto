from django.core.management.base import BaseCommand, CommandError
from clogethapp.models import Block, Transaction
import urllib.request
import json
from pprint import pprint
import os, io
import csv
# from web3.auto import w3
from web3 import Web3
# from web3.auto import w3
import json, sys, os
from web3.providers.rpc import HTTPProvider
import binascii
import json
import datetime
from hexbytes import HexBytes
from eth_utils import decode_hex
import time


# https://github.com/rabbit10086/allproject/blob/c21a0fd4a0b28f3d548c8ffed7b47fb3783eea73/IDCG_Auto/idcm/ethtes.py


class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)


def toDict(dictToParse):
    # convert any 'AttributeDict' type found to 'dict'
    parsedDict = dict(dictToParse)
    for key, val in parsedDict.items():
        # check for nested dict structures to iterate through
        if 'dict' in str(type(val)).lower():
            parsedDict[key] = toDict(val)
        # convert 'HexBytes' type to 'str'
        elif 'HexBytes' in str(type(val)):
            parsedDict[key] = val.hex()
    return parsedDict


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #  def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # pprint(w3.eth.blockNumber)
        # exit()
        w3 = Web3(HTTPProvider('http://gethnode:8545'))

        # if not w3.isConnected():
        if w3.isConnected() == False:
            exit("Нет соединения с блокчейном")
        if w3.eth.syncing != False:
            exit("Синхронизируется блокчейн")


# Хардфорк появится на блоке №1400000 в период с 11 по 12 ноября.
# Поэтому нет смысла перебирать другие блоки
#         pprint(w3.eth.getBlock(1400000))
        # pprint(w3.eth.blockNumber)
        # pprint(w3.eth.syncing.currentBlock)
        # pprint(w3.eth.syncing.highestBlock)
        # exit()
        i = 0
        i2 = 0
        block_first = 1400000
        block_last = w3.eth.blockNumber
        block_count = block_last - block_first

        for x in range(block_first, w3.eth.blockNumber):
            # pprint(str(round((i / block_count * 100),2))+"%")
            i = i + 1
            # print(str(x) + " из " + str(block_last))
            start_time_get_block = time.time()
            getblock = w3.eth.getBlock(x)
            pprint("BLOCK start_time_get_block: " + str((time.time() - start_time_get_block)))
            # pprint(block)
            # pprint(block['extraData'])
            # pprint(Web3.toText(block['extraData']))
            # pprint(block['transactions'].count)
            for trx_hash in getblock['transactions']:
                # pprint(x2)
                start_time_get_transaction_aaaa = time.time()
                aaaa = w3.eth.getTransactionReceipt(trx_hash)
                pprint("TX start_time_get_transaction_aaaa: " + str((time.time() - start_time_get_transaction_aaaa)))
                aaaa = dict(aaaa)
                # pprint(aaaa)

                start_time_get_transaction_bbbb = time.time()
                bbbb = w3.eth.getTransaction(trx_hash)
                pprint("TX start_time_get_transaction_bbbb: " + str((time.time() - start_time_get_transaction_bbbb)))

                bbbb = dict(bbbb)
                input_text = ''
                if aaaa['from'] == '0xd813419749b3c2cdc94a2f9cfcf154113264a9d6' or aaaa[
                    'to'] == '0xd813419749b3c2cdc94a2f9cfcf154113264a9d6':
                    # {'blockHash': HexBytes('0x27ca011db39fda4ef5a7746d75a4345955cc19da08cf724f1ea11ab1456101c3'),
                    #  'blockNumber': 1400053,
                    #  'contractAddress': None,
                    #  'cumulativeGasUsed': 63691,
                    #  'from': '0xa30d4c9699b5aa95bde5ed070cc37c75e9a8416c',
                    #  'gasUsed': 21691,
                    #  'logs': [],
                    #  'logsBloom': HexBytes(
                    #      '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'),
                    #  'status': 0,
                    #  'to': '0xd813419749b3c2cdc94a2f9cfcf154113264a9d6',
                    #  'transactionHash': HexBytes('0x7bb1037678f3420b0da3b5dd29a33fcda7155ef16727fa2109317b047ffb7f37'),
                    #  'transactionIndex': 2}
                    if bbbb['input'] == '0x1f288efb' or bbbb['input'] == '0x':
                        input_text = 'Deposit'
                    if bbbb['input'] == '0x4e71d92d':
                        input_text = 'Claim (Reward only)'
                    if bbbb['input'] == '0xcd948855':
                        input_text = 'Withdraw (Stake deposit + Reward)'

                    start_time_get_or_create = time.time()
                    obj, created = Transaction.objects.get_or_create(blockNumber=aaaa['blockNumber'],
                                                                     gasUsed=aaaa['gasUsed'],
                                                                     gas=bbbb['gas'],
                                                                     value=str(w3.fromWei(bbbb['value'], 'ether')),
                                                                         )
                    pprint("БД проверка записи: " + str((time.time() - start_time_get_or_create)))


                    if created:
                        pprint("запись не существовала " + str(aaaa['blockNumber']))
                        start_time_created = time.time()

                        obj.blockNumber=aaaa['blockNumber']
                        obj.status=aaaa['status']
                        obj.blockHash='0x' + str(binascii.b2a_hex(aaaa['blockHash'])).replace("b'", '').replace("'",
                                                                                                                '')
                        obj.tx='0x' + str(binascii.b2a_hex(aaaa['transactionHash'])).replace("b'",'').replace(
                                "'", '')
                        obj.addr_from=aaaa['from']
                        obj.addr_to=aaaa['to']
                        obj.gasUsed=aaaa['gasUsed']
                        obj.gas=bbbb['gas']
                        obj.gasPrice=bbbb['gasPrice']
                        obj.input=bbbb['input']
                        obj.input_text=input_text
                        obj.value=str(w3.fromWei(bbbb['value'], 'ether'))
                        obj.timestamp=getblock.timestamp
                        obj.save()
                        #
                        pprint("БД сохранение записи: " + str((time.time() - start_time_created)))
                    else:
                        pprint("запись существовала "+ str(aaaa['blockNumber']))

                    # exit(123)



                    # print("--- %s seconds ---" % (time.time() - start_time))
                    # pprint(aaaa)
                    # pprint(bbbb)
                    # created2 = Transaction.objects.get_or_create(
                    #     blockNumber=aaaa['blockNumber'],
                    #     status=aaaa['status'],
                    #     blockHash='0x' + str(binascii.b2a_hex(aaaa['blockHash'])).replace("b'", '').replace("'",
                    #                                                                                         ''),
                    #     tx='0x' + str(binascii.b2a_hex(aaaa['transactionHash'])).replace("b'",
                    #                                                                      '').replace(
                    #         "'", ''),
                    #     addr_from=aaaa['from'],
                    #     addr_to=aaaa['to'],
                    #     gasUsed=aaaa['gasUsed'],
                    #     gas=bbbb['gas'],
                    #     gasPrice=bbbb['gasPrice'],
                    #     input=bbbb['input'],
                    #     input_text=input_text,
                    #     value=str(w3.fromWei(bbbb['value'], 'ether')),
                    #     # timestamp=w3.eth.getBlock(aaaa['blockNumber']).timestamp,
                    #     timestamp=getblock.timestamp,
                    # )

                    # pprint(str('0x' + str(binascii.b2a_hex(aaaa['blockHash'])).replace("b'", '').replace("'",
                    #                                                                                         '')))
                    # pprint(str(w3.fromWei(bbbb['value'], 'ether')))

                    # exit()
                    # i2 = i2 + 1
                    # pprint(str(i) + ' ' + str(i2) + ' '
                    #        # + str(w3.eth.getBlock(aaaa['blockNumber']).timestamp)
                    #        + str(w3.eth.blockNumber) + ' '
                    #        + str(datetime.datetime.fromtimestamp(
                    #     w3.eth.getBlock(aaaa['blockNumber']).timestamp).isoformat())
                    #        + ' ' + str(w3.fromWei(bbbb['value'], 'ether')))
                    #
                    # pprint(aaaa)
                    # pprint('Адрес контракта')
                    # exit()


        # block=w3.eth.getBlock("0x246dbee1f0e3be212be2a4ca899a04924b78ae65b775132f301271dce7e1bd84")
        # # pprint(block)
        # pprint(block['extraData'])
        # pprint(Web3.toText(block['extraData']))

        # r =  w3.eth.getTransactionReceipt('0x66a81192b75703f9b983d0ac9bb61066aabc61c4048dfcdd44a649acae0b71fa')
        # r = dict(r)
        # # pprint(r)
        # logs = r['logs']
        # pprint(logs[0]['data'])
        # pprint(Web3.toText(r['logsBloom']))
        #
        # exit()


        self.stdout.write(self.style.SUCCESS('Successfully closed poll'))
