from milife_back.fitness.models import Weight, TargetWeight, Checkin
from milife_back.users.models import User


def remove_duplicate_weight(user):
    weights = Weight.objects.filter(user=user.id).order_by('-created_at')
    deleted = 0
    seen_dates = set()

    print(f'Total weight records: {len(weights)}')

    for weight in weights:
        if weight.measured_on in seen_dates:
            weight.delete()
            deleted += 1
        else:
            seen_dates.add(weight.measured_on)

    print(f'Deleted weight records: {deleted}')


def remove_duplicate_target_weight(user):
    weights = TargetWeight.objects.filter(user=user.id).order_by('-created_at')
    deleted = 0
    seen_dates = set()

    print(f'Total target weight records: {len(weights)}')

    for weight in weights:
        if weight.target_date in seen_dates:
            weight.delete()
            deleted += 1
        else:
            seen_dates.add(weight.target_date)

    print(f'Deleted target weight records: {deleted}')


def merge_duplicate_checkins(user):
    # Get all checkins that were created from the web app
    app_checkins = Checkin.objects.filter(user=user.id, accuniq_id='')

    for app_checkin in app_checkins:
        try:
            date_of_checkin = app_checkin.date_of_checkin

            # Get the duplicate checkin containing the accuniq data
            accuniq_checkin = Checkin.objects.exclude(accuniq_id='').get(user=user.id, date_of_checkin=date_of_checkin)

            app_checkin.accuniq_id = accuniq_checkin.accuniq_id
            app_checkin.accuniq_data = accuniq_checkin.accuniq_data
            app_checkin.accuniq_timestamp = accuniq_checkin.accuniq_timestamp

            accuniq_checkin.delete()
            app_checkin.save()
        except Checkin.DoesNotExist:
            pass
        except Exception as e:
            print(e)
            print(app_checkin)


if __name__ == '__main__':
    users = User.objects.all()

    for user in users:
        print(f'User: {user.first_name} {user.last_name} {user.id}')
        remove_duplicate_weight(user)
        remove_duplicate_target_weight(user)
        merge_duplicate_checkins(user)
