# Third Party Stuff
from django.contrib.auth import get_user_model, authenticate

# milife-back Stuff
from milife_back.base import exceptions as exc


def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise exc.WrongArguments("Invalid username/password. Please try again!")

    return user


def create_user_account(email, password, first_name="", last_name="", number="",):
    user = get_user_model().objects.create_user(
        email=email, password=password, first_name=first_name, last_name=last_name, number=number
    )
    return user

def invite_user(email, first_name, last_name):
    user = get_user_model().objects.create(
        email=email, first_name=first_name, last_name=last_name
    )
    return user


def get_user_by_email(email: str):
    return get_user_model().objects.filter(email__iexact=email).first()

def create_accuniq_id(first_name, last_name):
    last_name = f" {last_name}" if last_name.strip() != "" else ""
    return f"{first_name.upper()}{last_name.upper()}{'*'*20}"[:20]
