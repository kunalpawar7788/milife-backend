
## from datetime import timezone
from django.utils.dateparse import parse_datetime
import pytz
from milife_back.fitness.models import Checkin, AccuniqData
from milife_back.users.models import User

from datetime import datetime
import pytz

def populate_checkin_from_accuniq_data(accuniq_data_id=None):
    if accuniq_data_id:
        obj = AccuniqData.objects.get(id=accuniq_data_id)
    else:
        obj = AccuniqData.objects.order_by('-created_at').first()

    if not obj:
        return

    f = obj.csvfile.file
    f.seek(0)
    data = f.read().decode('utf-8')
    lines = data.split('\n')
    keys = list(map(str.strip, lines[0].split(',')))

    for row in lines[1:]:
        if len(row.strip()) == 0:
            continue

        values = list(map(str.strip, row.split(',')))
        record = dict(zip(keys, values))
        id_number = record['id_number'].replace('"','')

        try:
            user = User.objects.get(accuniq_id=id_number)
        except User.DoesNotExist:
            continue
        except User.MultipleObjectsReturned:
            print(id_number)
            continue

        date_str = str(record['received_date'])
        if len(date_str)==9:
            continue
        # date_str = f"0{date_str}" if len(date_str)==9 else date_str
        timestamp = datetime.strptime(date_str, "%y%m%d%H%M")
        localized = pytz.timezone('Europe/London').localize(timestamp, is_dst=None)

        try:
            checkin, created = Checkin.objects.get_or_create(
                date_of_checkin = localized.date(),
                accuniq_id = id_number,
                user=user
            )
        except Exception as e:
            print(e)
        else:
            if created:
                checkin.accuniq_data = record
                checkin.accuniq_timestamp = localized
            checkin.save()
