# Generated by Django 3.1 on 2020-10-26 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classnote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='classname',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
