from django.db import models

class Block(models.Model):
    block_hash = models.CharField(max_length=256)
    addr_from = models.CharField(max_length=256)
    addr_to = models.CharField(max_length=256)
    input_date = models.CharField(max_length=256)
    extraData = models.CharField(max_length=256)

class Transaction(models.Model):
    blockNumber = models.CharField(max_length=256)
    blockHash = models.CharField(max_length=256)
    tx = models.CharField(max_length=256)
    addr_from = models.CharField(max_length=256)
    addr_to = models.CharField(max_length=256)
    gasUsed = models.CharField(max_length=256)
    gas = models.CharField(max_length=256)
    gasPrice = models.CharField(max_length=256)
    input = models.CharField(max_length=256)
    input_text = models.CharField(max_length=256)
    value = models.CharField(max_length=256)
    timestamp = models.IntegerField(default=0)




