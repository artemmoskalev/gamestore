from django.contrib.auth.models import User

from restapi.models import ApiKey

api_key_size = 64

def make_and_get_key(user):
    try:
        user.key
    except:
        make_key_for(user)    

    return user.key.key


def make_key_for(user):
    key = User.objects.make_random_password(length=api_key_size)

    while ApiKey.objects.filter(key__exact=key).count():
        key = User.objects.make_random_password(length=api_key_size)

    new_api_key = ApiKey(user = user, key=key)
    new_api_key.save()
    return new_api_key

