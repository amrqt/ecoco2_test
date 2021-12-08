from django.db import models

# Create your models here.
class CO2DataModel(models.Model):
    """ Provice storage for CO2 rates data
    """

    name = models.TextField(null=False)
    start_date = models.BigIntegerField(null=False)
    end_date = models.BigIntegerField(null=False)
    data = models.JSONField(null=False)