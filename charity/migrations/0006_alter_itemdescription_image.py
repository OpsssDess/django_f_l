# Generated by Django 4.0.6 on 2022-11-22 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0005_alter_donation_status_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdescription',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/'),
        ),
    ]