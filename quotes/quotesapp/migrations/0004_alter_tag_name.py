# Generated by Django 5.0 on 2023-12-31 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotesapp', '0003_author_user_quote_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=35, unique=True),
        ),
    ]
