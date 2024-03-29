# Generated by Django 4.0 on 2022-01-06 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uitslag',
            options={'ordering': ('race__startdate', 'rank'), 'verbose_name_plural': 'Uitslagen'},
        ),
        migrations.AlterField(
            model_name='uitslag',
            name='rank',
            field=models.IntegerField(max_length=3),
        ),
        migrations.AlterUniqueTogether(
            name='uitslag',
            unique_together={('race', 'rank')},
        ),
    ]
