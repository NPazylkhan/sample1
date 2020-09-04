# Generated by Django 2.2.6 on 2019-10-24 07:19

import bboard.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bboard', '0001_initial_squashed_0003_auto_20191014_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='bb',
            name='kind',
            field=models.CharField(choices=[(None, 'Choose advertise'), ('buy', 'Buy'), ('sell', 'Sell'), ('change', 'Change')], default=1, max_length=10, verbose_name='Some Kind of Choises'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bb',
            name='price',
            field=models.FloatField(blank=True, null=True, validators=[bboard.models.validate_even], verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='bb',
            name='title',
            field=models.CharField(error_messages={'invalid': 'error name of goods, Bakarayo'}, max_length=50, validators=[django.core.validators.RegexValidator(regex='^.{4,}$')], verbose_name='Goods'),
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('spares', models.ManyToManyField(to='bboard.Sp')),
            ],
        ),
        migrations.CreateModel(
            name='AdvUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_activated', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
