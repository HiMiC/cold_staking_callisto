from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from web3 import Web3
# from web3.auto import w3
import json, sys, os
from web3.providers.rpc import HTTPProvider
import binascii
import json
import datetime
from hexbytes import HexBytes
from eth_utils import decode_hex
# Create your views here.
from .models import Block, Transaction

from decimal import Decimal
from pprint import pprint
import environ

env = environ.Env(DEBUG=(bool, False), )
environ.Env.read_env('.env')


def post_home(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:4]
    # news = News.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:4]
    # sliders = SliderHome.objects.filter(is_enable=True).order_by('-published_date')[:4]
    # gallery = Photo.objects.all()[:4]

    title = 'Callisto Network statistic'
    keywords = 'Callisto Network'

    geth_host = 'http://' + env('GETH_HOST', default='gethnode') + ':' + env('GETH_PORT', default='8545')
    w3 = Web3(HTTPProvider(geth_host))
    if w3.isConnected() == False:
        exit("Нет соединения с блокчейном " + geth_host)
    else:
        pprint("Успешно подключились к " + geth_host)

    block_height = w3.eth.blockNumber
    last_block = w3.eth.getBlock(block_height)

    block_time = (last_block.timestamp - w3.eth.getBlock(block_height - 100).timestamp) / 100;

    # blockTime = (docs[0].timestamp - docs[99].timestamp) / 100;
    # hashrate = docs[0].difficulty / blockTime;
    hashrate = last_block.difficulty / 100

    difficulty = w3.eth.getBlock(w3.eth.blockNumber).difficulty

    block_height = w3.eth.syncing.highestBlock

    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
        'block_height': block_height,
        'difficulty': difficulty,
        'block_time': block_time,
        'hashrate': hashrate,
    })


def block_list(request, pk):
    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
    })


def block(request, pk):
    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    geth_host = 'http://' + env('GETH_HOST', default='gethnode') + ':' + env('GETH_PORT', default='8545')
    w3 = Web3(HTTPProvider(geth_host))
    if w3.isConnected() == False:
        exit("Нет соединения с блокчейном " + geth_host)
    else:
        pprint("Успешно подключились к " + geth_host)
    pprint(pk)


    try:
        getblock = w3.eth.getBlock(int(pk))

        if getblock == None:
            print('pass')
            raise TypeError
    except TypeError:
        raise Http404("Poll does not exist")


    if getblock == None:
        html = "<html><body>404</body></html>"
        return HttpResponse(html)
        # exit(404)

    pprint(getblock)

    # getblock2 = getblock.copy
    # getblock2['totalDifficulty'] = 123
    get_block = getblock
    # get_block['totalDifficulty'] = 123


    get_transactions = getblock['transactions']
    # get_transactions = dict(gettransactions)
    # pprint(get_transactions)
    # pprint(get_block)
    # exit()
    for trx_hash in getblock['transactions']:
        pprint(trx_hash)
        # aaaa = w3.eth.getTransactionReceipt(trx_hash)
        # pprint(aaaa)
        # bbbb = w3.eth.getTransaction(trx_hash)
        # pprint(bbbb)

    # exit()


    return render(request, 'block.html', {
        'title': title,
        'keywords': keywords,
        'get_block': get_block,
        'get_transactions': get_transactions,
    })



def tx(request, pk):
    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
    })


def tx_list(request, pk):
    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
    })


def addr(request, pk):
    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
    })


def stat(request, pk):
    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
    })


def getDifficulty(hashes):
    result = 0
    unit = ''

    if hashes != 0 and hashes < 1000:
        result = hashes
        unit = ''

    if hashes >= 1000 and hashes < math.pow(1000, 2):
        result = hashes / 1000
        unit = 'K'

    if hashes >= math.pow(1000, 2) and hashes < math.pow(1000, 3):
        result = hashes / math.pow(1000, 2)
        unit = 'M'

    if hashes >= math.pow(1000, 3) and hashes < math.pow(1000, 4):
        result = hashes / math.pow(1000, 3)
        unit = 'G'

    if hashes >= math.pow(1000, 4):
        result = hashes / math.pow(1000, 4)
        unit = 'T'

    # return str(Decimal(result).normalize()) + ' ' + unit + 'H'
    return str('{0:.2f}'.format(result).rstrip('0').rstrip('.')) + ' ' + unit + 'H'
