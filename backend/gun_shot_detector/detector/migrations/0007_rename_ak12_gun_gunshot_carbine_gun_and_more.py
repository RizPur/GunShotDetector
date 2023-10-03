# Generated by Django 4.2.5 on 2023-09-23 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detector', '0006_alter_gunshotdetector_latitude_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gunshot',
            old_name='ak12_gun',
            new_name='carbine_gun',
        ),
        migrations.RenameField(
            model_name='gunshot',
            old_name='imi_desert_eagle_gun',
            new_name='pistol_gun',
        ),
        migrations.RenameField(
            model_name='gunshot',
            old_name='m4_gun',
            new_name='revolver_gun',
        ),
        migrations.RemoveField(
            model_name='gunshot',
            name='other_gun',
        ),
    ]