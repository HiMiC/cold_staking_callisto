from django.db import models

class Block(models.Model):
    block_hash = models.CharField(max_length=256)
    addr_from = models.CharField(max_length=256)
    addr_to = models.CharField(max_length=256)
    input_date = models.CharField(max_length=256)
    extraData = models.CharField(max_length=256)

class Transaction(models.Model):
    blockNumber = models.CharField(max_length=256)
    status = models.IntegerField(default=0)
    blockHash = models.CharField(max_length=256)
    tx = models.CharField(max_length=256)
    addr_from = models.CharField(max_length=256,db_index=True)
    addr_to = models.CharField(max_length=256,db_index=True)

    gasUsed = models.IntegerField(blank=True, null=True)
    gas = models.IntegerField(blank=True, null=True)
    gasPrice = models.BigIntegerField(blank=True, null=True)

    input = models.CharField(max_length=256)
    input_text = models.CharField(max_length=256)
    value = models.FloatField(blank=True, null=True)
    timestamp = models.IntegerField(default=0)
    class Meta:
        index_together = ["blockNumber", "gasUsed", "gas", "value"]




