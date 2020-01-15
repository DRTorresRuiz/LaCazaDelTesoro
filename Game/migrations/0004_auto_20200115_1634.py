# Generated by Django 2.2.8 on 2020-01-15 16:34

from django.db import migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0003_game_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='address_center',
            field=geoposition.fields.GeopositionField(max_length=42),
        ),
    ]