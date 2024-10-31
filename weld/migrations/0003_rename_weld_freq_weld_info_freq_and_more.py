# Generated by Django 5.1.2 on 2024-10-20 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0002_weld_info_seleted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weld_info',
            old_name='weld_freq',
            new_name='freq',
        ),
        migrations.RenameField(
            model_name='weld_info',
            old_name='weld_length',
            new_name='length',
        ),
        migrations.RenameField(
            model_name='weld_info',
            old_name='weld_power',
            new_name='power',
        ),
        migrations.RenameField(
            model_name='weld_info',
            old_name='weld_program',
            new_name='program',
        ),
        migrations.RenameField(
            model_name='weld_info',
            old_name='seleted',
            new_name='selected',
        ),
        migrations.RenameField(
            model_name='weld_raw_data',
            old_name='weld_freq',
            new_name='freq',
        ),
        migrations.RenameField(
            model_name='weld_raw_data',
            old_name='weld_length',
            new_name='length',
        ),
        migrations.RenameField(
            model_name='weld_raw_data',
            old_name='weld_power',
            new_name='power',
        ),
    ]
