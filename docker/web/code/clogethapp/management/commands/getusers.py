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
        w3 = Web3(HTTPProvider('http://192.168.1.240:8545'))
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

        fname = "0xd813419749b3c2cdc94a2f9cfcf154113264a9d6-transactions-1554288562.csv"
        if os.path.isfile(fname):
            pprint('Фаил существует ' + fname)

            i = 0
            i2 = 0

            with open(fname, 'r', newline='') as csvfile:

                spamreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
                for row in spamreader:
                    block = row[0]
                    # pprint(block)
                    getblock = w3.eth.getBlock(block)


                    extraData = str(w3.eth.getBlock(w3.eth.blockNumber)['extraData']).replace("b'", '').replace("'",'')
                    created = Block.objects.get_or_create(
                        block_hash=row[0],
                        addr_from=row[1],
                        addr_to=row[2],
                        input_date=row[3],
                        extraData=extraData,

                    )

                    i = i + 1

                    if getblock is None:
                        pprint(getblock)
                        exit('NOT getblock')

                    gettransactions = getblock.transactions
                    # pprint(getblock.transactions)

                    for trx_hash in gettransactions:

                        aaaa = w3.eth.getTransactionReceipt(trx_hash)
                        bbbb = w3.eth.getTransaction(trx_hash)
                        bbbb = dict(bbbb)
                        input_text = ''
                        if aaaa['from'] == '0xd813419749b3c2cdc94a2f9cfcf154113264a9d6' or aaaa[
                            'to'] == '0xd813419749b3c2cdc94a2f9cfcf154113264a9d6':
                            if bbbb['input'] == '0x1f288efb' or bbbb['input'] == '0x':
                                input_text = 'Deposit'
                            if bbbb['input'] == '0x4e71d92d':
                                input_text = 'Claim (Reward only)'
                            if bbbb['input'] == '0xcd948855':
                                input_text = 'Withdraw (Stake deposit + Reward)'

                            created2 = Transaction.objects.get_or_create(
                                blockNumber=aaaa['blockNumber'],
                                blockHash='0x' + str(binascii.b2a_hex(aaaa['blockHash'])).replace("b'", '').replace("'",
                                                                                                                    ''),
                                tx='0x' + str(binascii.b2a_hex(aaaa['transactionHash'])).replace("b'",
                                                                                                 '').replace(
                                    "'", ''),
                                addr_from=aaaa['from'],
                                addr_to=aaaa['to'],
                                gasUsed=aaaa['gasUsed'],
                                gas=bbbb['gas'],
                                gasPrice=bbbb['gasPrice'],
                                input=bbbb['input'],
                                input_text=input_text,
                                value=str(w3.fromWei(bbbb['value'], 'ether')),
                                # timestamp=w3.eth.getBlock(aaaa['blockNumber']).timestamp,
                                timestamp=getblock.timestamp,
                            )
                            i2 = i2 + 1
                            pprint(str(i) + ' ' + str(i2) + ' '
                                   # + str(w3.eth.getBlock(aaaa['blockNumber']).timestamp)
                                    + str(w3.eth.blockNumber) +' '
                                   + str(datetime.datetime.fromtimestamp(
                                w3.eth.getBlock(aaaa['blockNumber']).timestamp).isoformat())
                                   + ' ' + str(w3.fromWei(bbbb['value'], 'ether')))





        else:
            pprint('Фаил не существует ' + fname)

        self.stdout.write(self.style.SUCCESS('Successfully closed poll'))
