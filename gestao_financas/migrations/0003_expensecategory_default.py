# Generated by Django 4.2.2 on 2023-06-19 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_financas', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensecategory',
            name='default',
            field=models.BooleanField(null=True),
        ),
    ]
