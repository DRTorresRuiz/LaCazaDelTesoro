from djongo import models

## INFO ABOUT MODELS:
    # https://docs.djangoproject.com/en/2.2/ref/models/instances/
    # https://docs.djangoproject.com/en/2.2/topics/db/models/
    # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/select_some_fields.html

## Create your models here.

# Create a Manager if you need to control how a model instance is created and selected.
    # class UserManager(models.Manager):
    #     def createUser(self, name):
    #         user = self.create(id=2, name=name)
    #         return user

# Models
    # class User(models.Model):
    #     # _id is autocreated.
    #     name = models.CharField(max_length=100)
        
    #     objects = UserManager()

    #     def __str__(self):
    #         return self.name
