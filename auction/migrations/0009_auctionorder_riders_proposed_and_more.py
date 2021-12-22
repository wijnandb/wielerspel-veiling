# Generated by Django 4.0 on 2021-12-22 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0008_auto_20211206_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionorder',
            name='riders_proposed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='auctionorder',
            name='team_captain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.teamcaptain'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='team_captain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.teamcaptain'),
        ),
        migrations.AlterField(
            model_name='joker',
            name='team_captain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.teamcaptain'),
        ),
        migrations.AlterField(
            model_name='tobeauctioned',
            name='team_captain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auction.teamcaptain'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='virtualteam',
            name='ploegleider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.teamcaptain'),
        ),
    ]
