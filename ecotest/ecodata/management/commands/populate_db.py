from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from ecotest.ecodata.models import CO2DataModel
import requests

class Command(BaseCommand):
    help = 'Fetch CO2 rates and populate db'

    def handle(self, *args, **options):
        start_date = datetime(2017, 1, 1, 0, 0).timestamp()
        end_date = datetime(2018, 12, 31, 23, 59).timestamp()
        url = 'http://api-recrutement.ecoco2.com/v1/data/?start={}&end={}'.format(start_date, end_date)

        
        if len(CO2DataModel.objects.all()) > 0:
            self.stdout.write(self.style.SUCCESS('Database already contains CO2 rates data'))
            return

        resp = requests.get(url)

        co2data = CO2DataModel(
            name='co2data',
            start_date=start_date,
            end_date=end_date,
            data=resp.json()
        )

        co2data.save()

        self.stdout.write(self.style.SUCCESS('Successfully fetched CO2 rates data'))