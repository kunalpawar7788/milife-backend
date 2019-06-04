import pandas as pd

## from datetime import timezone
from django.utils.dateparse import parse_datetime
import pytz
from milife_back.fitness.models import Checkin, AccuniqData
from milife_back.users.models import User

from datetime import datetime
import pandas as pd
import pytz

def populate_checkin_from_accuniq_data(accuniq_data_id):
    obj = AccuniqData.objects.get(id=accuniq_data_id)
    df = pd.read_csv(obj.csvfile)
    df.rename(columns=df.iloc[0]).drop(df.index[0])
    records = df.to_dict('index')
    records_count = len(df)
    for key in records:
        record = records[key]

        try:
            user = User.objects.get(accuniq_id=record['id_number'])
        except User.DoesNotExist:
            user = None

        date_str = str(record['received_date'])

        date_str = f"0{date_str}" if len(date_str)==9 else date_str
        timestamp = datetime.strptime(date_str, "%y%m%d%H%M")
        localized = pytz.timezone('Europe/London').localize(timestamp, is_dst=None)

        try:
            checkin, created = Checkin.objects.get_or_create(
                accuniq_timestamp = localized,
                accuniq_id = record['id_number']
            )
        except Exception as e:
            print(e)
        else:
            checkin.user = user
            if created:
                checkin.accuniq_data = record
                checkin.date_of_checkin = localized.date()
            checkin.save()


