from django import template
import math

register = template.Library()

import time
import timeago, datetime
from datetime import datetime

@register.filter(name='print_timestamp')
def print_timestamp(timestamp):
    now = datetime.now()
    date = datetime.fromtimestamp(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S %z", time.gmtime(timestamp)) +" (" +timeago.format(date, now, 'en')+")"

@register.filter(name='getDifficulty')
def getDifficulty(hashes): # Only one argument.
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