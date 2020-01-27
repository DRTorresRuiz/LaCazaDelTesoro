# Generated by Django 2.2.8 on 2020-01-26 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0004_player_treasure_found_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='address_center',
        ),
        migrations.AlterField(
            model_name='player_treasure_found',
            name='treasure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treasure', to='Game.Treasure'),
        ),
    ]
