# Generated by Django 2.2.8 on 2019-12-20 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0002_auto_20191220_0549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='geolocation_center',
            new_name='position',
        ),
        migrations.RenameField(
            model_name='treasure',
            old_name='geolocation',
            new_name='position',
        ),
    ]