from django.core.management.base import BaseCommand, CommandError
from clogethapp.models import Block, Transaction, Account
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
import environ
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env('.env')

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

        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        # pprint(w3.eth.blockNumber)
        # exit()
        geth_host = 'http://'+env('GETH_HOST', default='gethnode')+':'+env('GETH_PORT', default='8545')
        # geth_host = 'http://95.129.164.103:8545'
        # geth_host = 'http://192.168.1.150:8545'
        w3 = Web3(HTTPProvider(geth_host))
        # exit()
        # if not w3.isConnected():
        if w3.isConnected() == False:
            exit(FAIL + "Нет соединения с блокчейном " + geth_host + ENDC)
        else:
            pprint("Успешно подключились к " + geth_host)

        if w3.eth.syncing != False:
            # pprint(w3.eth.blockNumber)
            # pprint(w3.eth.syncing)
            # pprint(w3.eth.syncing.currentBlock)
            # pprint(w3.eth.syncing.highestBlock)

            procent = str(round((w3.eth.syncing.currentBlock / w3.eth.syncing.highestBlock * 100), 2)) + "%"

            exit(WARNING + "ОСТАНОВЛЕНО Синхронизируется блокчейн до текущего состояния: " + procent
                 +" - "+str(w3.eth.syncing.currentBlock) +" из "
                 + str(w3.eth.syncing.highestBlock)
                 +ENDC)

        # Хардфорк появится на блоке №1400000 в период с 11 по 12 ноября.
        # Поэтому нет смысла перебирать другие блоки
        #         pprint(w3.eth.getBlock(1400000))

        i = 0
        # если база не пустая то берем последний блок
        if Transaction.objects.all().count():
            f_first = Transaction.objects.order_by('blockNumber').reverse()[0]
            pprint("Последняя запись в базе "+str(f_first.blockNumber))
            block_first = f_first.blockNumber
        else:
            block_first = 0
            # block_first = 1

        pprint(str(block_first) + " - Первый блок для парсинга")
        # block_first = 1826493 #остановил
        block_last = w3.eth.blockNumber
        pprint(str(block_last) + " - Текщий блок ")
        block_count = block_last - block_first
        if block_last <= block_first:
            pprint("Синхронизация не возможна. Блокчейн (блок (" + str(
                block_last) + ") не синхронизировался до блока " + str(block_first))

        debug = 0
        debug2 = 0

        for x in range(block_first, w3.eth.blockNumber):

            pprint(str(round((i / block_count * 100), 2)) + "%")
            i = i + 1
            # print(str(x) + " из " + str(block_last))
            start_time_get_block = time.time()
            getblock = w3.eth.getBlock(x)
            if debug2:
                pprint("BLOCK get_block: " + str((time.time() - start_time_get_block)))

            for trx_hash in getblock['transactions']:
                # pprint(x2)
                start_time_get_transaction_aaaa = time.time()
                aaaa = w3.eth.getTransactionReceipt(trx_hash)
                if debug2:
                    pprint(
                        "TX start_time_get_transaction_aaaa: " + str((time.time() - start_time_get_transaction_aaaa)))
                aaaa = dict(aaaa)
                # pprint(aaaa)

                start_time_get_or_create = time.time()

                obj, created = Account.objects.get_or_create(addr=aaaa['from'],)
                if created:
                    if debug:
                        pprint("запись не существовала " + str(aaaa['blockNumber']))
                    obj.balance = w3.fromWei(w3.eth.getBalance(w3.toChecksumAddress(aaaa['from'])), 'ether')
                    obj.save()

                obj2, created2 = Account.objects.get_or_create(addr=aaaa['to'],)
                if created2:
                    if debug:
                        pprint("запись не существовала " + str(aaaa['blockNumber']))
                    obj2.balance = w3.fromWei(w3.eth.getBalance(w3.toChecksumAddress(aaaa['to'])), 'ether')
                    obj2.save()

                # else:
                #     obj.blockNumber = aaaa['blockNumber']
                #     obj.save()


                if debug:
                    pprint("БД проверка записи: " + str((time.time() - start_time_get_or_create)))

                        #

                        # exit()

            pprint("BLOCK END: " + str((time.time() - start_time_get_block)))

        self.stdout.write(self.style.SUCCESS('Successfully closed poll'))
