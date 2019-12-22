# Generated by Django 2.2.8 on 2019-12-22 11:58

import Game.models
from django.db import migrations
import django_enum_choices.choice_builders
import django_enum_choices.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0005_treasure_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='status',
            field=django_enum_choices.fields.EnumChoiceField(choice_builder=django_enum_choices.choice_builders.value_value, choices=[('Finalized', 'Finalized'), ('In Progresss', 'In Progresss')], default=Game.models.Status('In Progresss'), enum_class=Game.models.Status, max_length=12),
        ),
    ]
