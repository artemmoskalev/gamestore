from django.contrib.auth.models import User, Group, Permission, ContentType
from django.contrib import auth

def save_sosial_account_as_player(strategy, user, response, details,
                         is_new=False,*args,**kwargs):
    
    if(user):

        playersGroup, isCreated = Group.objects.get_or_create(name="players")

        if isCreated:
            content_type = ContentType.objects.get(app_label='gamedata', model='game')
            playPermission = Permission.objects.get_or_create(name="Can Play", codename="can_play", content_type=content_type)
            playersGroup.permissions.add(playPermission[0])
                                                    
        playersGroup.user_set.add(user) 
    
        