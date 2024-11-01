# Generated by Django 5.1.2 on 2024-10-19 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weld_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=10)),
                ('weld_program', models.CharField(max_length=10)),
                ('weld_power', models.IntegerField()),
                ('weld_freq', models.FloatField()),
                ('weld_length', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Weld_raw_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('model_id', models.IntegerField()),
                ('model_name', models.CharField(max_length=10)),
                ('result', models.BooleanField()),
                ('weld_power', models.IntegerField()),
                ('weld_freq', models.FloatField()),
                ('weld_length', models.FloatField()),
            ],
        ),
    ]
