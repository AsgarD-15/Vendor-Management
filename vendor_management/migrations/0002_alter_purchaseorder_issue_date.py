# Generated by Django 5.0 on 2023-12-08 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='issue_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]