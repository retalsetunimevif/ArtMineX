# Generated by Django 4.2.4 on 2023-08-13 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArtMineX', '0012_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
