# Generated by Django 2.1.4 on 2018-12-15 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colleges', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'managed': False, 'ordering': ['city_name'], 'verbose_name': 'city', 'verbose_name_plural': 'cities'},
        ),
        migrations.AlterModelOptions(
            name='graduationracetype',
            options={'managed': False, 'ordering': ['race_category_name'], 'verbose_name': 'IPEDS Institution Graduation Race Type', 'verbose_name_plural': 'IPEDS Institution Graduation Race Types'},
        ),
        migrations.AlterModelOptions(
            name='state',
            options={'managed': False, 'ordering': ['state_name'], 'verbose_name': 'state', 'verbose_name_plural': 'states'},
        ),
    ]