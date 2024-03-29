# Generated by Django 4.0 on 2022-01-05 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamCaptain',
            fields=[
                ('team_captain', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('order', models.IntegerField(default=0)),
                ('riders_proposed', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['riders_proposed', 'order'],
            },
        ),
        migrations.CreateModel(
            name='VirtualTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('editie', models.PositiveIntegerField(default=2022)),
                ('price', models.IntegerField(default=0)),
                ('punten', models.FloatField(default=0)),
                ('jpp', models.IntegerField(default=0)),
                ('ploegleider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='results.rider')),
            ],
            options={
                'verbose_name_plural': 'Virtual Teams',
                'ordering': ['-price'],
            },
        ),
        migrations.CreateModel(
            name='Joker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='results.rider')),
                ('team_captain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'ordering': ['team_captain'],
            },
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rider', to='results.rider')),
                ('team_captain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='ToBeAuctioned',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=100000)),
                ('amount', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('sold', models.BooleanField(default=False)),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='results.rider')),
                ('team_captain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'ordering': ['order', 'modified'],
                'unique_together': {('team_captain', 'rider')},
            },
        ),
    ]
