from djongo import models

# https://docs.djangoproject.com/en/2.2/ref/models/instances/
# https://docs.djangoproject.com/en/2.2/topics/db/models/
# https://books.agiliq.com/projects/django-orm-cookbook/en/latest/select_some_fields.html

# Create your models here.
class UserManager(models.Manager):
    def createUser(self, name):
        user = self.create(id=2, name=name)
        return user

class User(models.Model):
    id =  models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    
    objects = UserManager()

    def __str__(self):
        return self.name
