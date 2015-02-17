from django.db import models
from django.contrib.auth.models import User
import uuid

class RegistrationKey(models.Model):
    auth_key = models.CharField(max_length=100, null=False, blank=False, unique=True)
    registered_user = models.ForeignKey(User, null=False, blank=False)
    
    def createUniqueKey(self):
        self.auth_key = str(uuid.uuid4())