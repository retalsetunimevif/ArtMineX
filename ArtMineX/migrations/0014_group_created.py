# Generated by Django 4.2.4 on 2023-08-14 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArtMineX', '0013_alter_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default='2023-08-14'),
            preserve_default=False,
        ),
    ]
