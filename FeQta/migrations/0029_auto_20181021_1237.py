# Generated by Django 2.0.7 on 2018-10-21 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FeQta', '0028_auto_20181020_1647'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-score']},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-updated', '-timestamp']},
        ),
        migrations.AlterField(
            model_name='profile',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
