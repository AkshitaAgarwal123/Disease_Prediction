from django.db import models

class UserDb(models.Model):
    username = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)

    def __str__(self):
        return self.username+" "+self.password
