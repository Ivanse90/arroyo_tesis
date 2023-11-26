# Generated by Django 4.2 on 2023-06-06 03:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_data_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='history_tweet',
            name='id_data',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history_tweet',
            name='tweet_text',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]