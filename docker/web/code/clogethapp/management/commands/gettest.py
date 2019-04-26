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
        debug = 1
        debug2 = 0

        aaaa = w3.eth.getTransactionReceipt('0x6ba2d7f8a25d0291e5cd774d09a8f1b1b3b5b9455c6dc3c970a8447f2e692979')
        aaaa = dict(aaaa)
        pprint(aaaa)
        bbbb = w3.eth.getTransaction('0x6ba2d7f8a25d0291e5cd774d09a8f1b1b3b5b9455c6dc3c970a8447f2e692979')
        bbbb = dict(bbbb)
        pprint(bbbb)

        pprint(w3.toChecksumAddress('0x0073cf1b9230cf3ee8cab1971b8dbef21ea7b595'))
        pprint(w3.eth.getBalance(w3.toChecksumAddress('0x0073cf1b9230cf3ee8cab1971b8dbef21ea7b595')))
        # pprint(w3.eth.getBalance(w3.toChecksumAddress('0xae555ddf81a00061716f0b50a4ad5f2449c42bb1'),1593176))
        r, r2 = w3.manager.request_blocking( "eth_getBalance",[w3.toChecksumAddress('0x0073cf1b9230cf3ee8cab1971b8dbef21ea7b595'), 255683],)
        pprint(r)
        pprint(r2)

        # pprint(w3.fromWei(w3.eth.getBalance(w3.toChecksumAddress('0xae555ddf81a00061716f0b50a4ad5f2449c42bb1')), 'ether'))

        # pprint(w3.eth.getBalance('0xae555ddf81a00061716f0b50a4ad5f2449c42bb1', 1415068))
        # pprint(w3.eth.getBalance('0xae555ddf81a00061716f0b50a4ad5f2449c42bb1', 1593172))
        # pprint(w3.eth.getBalance('0xae555ddf81a00061716f0b50a4ad5f2449c42bb1', 1593176))


        exit()
        for x in range(block_first, w3.eth.blockNumber):

            pprint(str(round((i / block_count * 100),2))+"%")
            i = i + 1
            # print(str(x) + " из " + str(block_last))
            start_time_get_block = time.time()
            getblock = w3.eth.getBlock(x)
            if debug2:
                pprint("BLOCK get_block: " + str((time.time() - start_time_get_block)))
            # pprint(block)
            # pprint(block['extraData'])
            # pprint(Web3.toText(block['extraData']))
            # pprint(block['transactions'].count)
            for trx_hash in getblock['transactions']:
                # pprint(x2)
                start_time_get_transaction_aaaa = time.time()
                aaaa = w3.eth.getTransactionReceipt(trx_hash)
                if debug2:
                    pprint("TX start_time_get_transaction_aaaa: " + str((time.time() - start_time_get_transaction_aaaa)))
                aaaa = dict(aaaa)
                # pprint(aaaa)


                if aaaa['from'] == '0xd813419749b3c2cdc94a2f9cfcf154113264a9d6' or aaaa[
                    'to'] == '0xd813419749b3c2cdc94a2f9cfcf154113264a9d6':
                    # pprint(aaaa)
                    # pprint(aaaa['transactionIndex'])
                    # exit()
                    # pprint(bbbb)
                    start_time_get_transaction_bbbb = time.time()
                    bbbb = w3.eth.getTransaction(trx_hash)
                    if debug2:
                        pprint("TX start_time_get_transaction_bbbb: " + str(
                            (time.time() - start_time_get_transaction_bbbb)))

                    bbbb = dict(bbbb)
                    input_text = ''
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
                    pprint(bbbb['transactionIndex'])
                    pprint(type(bbbb['transactionIndex']))
                    # exit()
                    obj, created = Transaction.objects.get_or_create(blockNumber=aaaa['blockNumber'],
                                                                     transactionIndex=bbbb['transactionIndex'],
                                                                     # value=str(w3.fromWei(bbbb['value'], 'ether'))
                                                                    )
                    # obj, created = Transaction.objects.get_or_create(blockNumber=aaaa['blockNumber'],
                    #                                                  gasUsed=aaaa['gasUsed'],
                    #                                                  gas=bbbb['gas'],
                    #                                                  value=str(w3.fromWei(bbbb['value'], 'ether')),
                    #                                                      )
                    pprint("БД проверка записи: " + str((time.time() - start_time_get_or_create)))


                    if created:
                        pprint("запись не существовала " + str(aaaa['blockNumber']))
                        start_time_created = time.time()

                        obj.blockNumber=aaaa['blockNumber']
                        obj.transactionIndex=bbbb['transactionIndex']
                        obj.contractAddress=aaaa['contractAddress']

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
                        # obj.value=str(w3.fromWei(bbbb['value'], 'ether'))
                        obj.value=str(w3.fromWei(bbbb['value'], 'ether'))
                        obj.timestamp=getblock.timestamp
                        obj.save()
                        #
                        pprint(bbbb['value'])
                        pprint(type(bbbb['value']))

                        pprint(str(w3.fromWei(bbbb['value'], 'ether')))
                        pprint(type(str(w3.fromWei(bbbb['value'], 'ether'))))

                        pprint("БД сохранение записи: " + str((time.time() - start_time_created)))
                    else:
                        pprint(aaaa)
                        pprint(bbbb)
                        pprint("запись существовала "+ str(aaaa['blockNumber']))
                        pprint("Проверка индексов в БД. при новом запуске чистой бд не должно быть повторяющихся blockNumber, gasUsed, gas, value")
                        pprint("Значит значение не уникальное")
                        pprint("Переписать индексы")
                        exit()

            pprint("BLOCK END: " + str((time.time() - start_time_get_block)))







        self.stdout.write(self.style.SUCCESS('Successfully closed poll'))
