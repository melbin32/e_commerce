# Generated by Django 4.1.4 on 2023-01-07 04:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listing_category_user_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='highest_bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]