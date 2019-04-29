from django.db import models

class Block(models.Model):
    block_hash = models.CharField(max_length=70)
    addr_from = models.CharField(max_length=42)
    addr_to = models.CharField(max_length=42)
    input_date = models.CharField(max_length=256)
    extraData = models.CharField(max_length=256)

class Account(models.Model):
    addr = models.CharField(max_length=42,db_index=True)
    balance = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=256,blank=True, null=True)
    blockNumber = models.IntegerField(blank=True, null=True)

class Csbalance(models.Model):
    blockNumber = models.IntegerField(db_index=True)
    balance = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=256)

class Transaction(models.Model):
    blockNumber = models.IntegerField()
    transactionIndex = models.IntegerField(blank=True, null=True)

    status = models.IntegerField(blank=True, null=True)
    blockHash = models.CharField(max_length=70)

    contractAddress = models.CharField(max_length=256,db_index=True,blank=True, null=True)
    tx = models.CharField(max_length=66)
    addr_from = models.CharField(max_length=42,db_index=True)
    addr_to = models.CharField(max_length=42,db_index=True)

    gasUsed = models.IntegerField(blank=True, null=True)
    gas = models.IntegerField(blank=True, null=True)
    gasPrice = models.BigIntegerField(blank=True, null=True)

    input = models.CharField(max_length=256)
    input_text = models.CharField(max_length=256)
    value = models.FloatField(blank=True, null=True)
    timestamp = models.IntegerField(default=0)

    class Meta:
        index_together = ["blockNumber", "transactionIndex"]




