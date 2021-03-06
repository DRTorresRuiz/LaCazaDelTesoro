# Generated by Django 2.2.8 on 2020-01-23 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner_game', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='address_center',
            field=geoposition.fields.GeopositionField(max_length=42),
        ),
        migrations.AlterField(
            model_name='treasure',
            name='treasure_img',
            field=models.ImageField(blank=True, null=True, upload_to='treasure/%Y/%m/%d'),
        ),
    ]
