# Generated by Django 4.0.6 on 2022-10-16 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0006_alter_good_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='state',
            field=models.CharField(choices=[('requested', 'requested'), ('available', 'available'), ('booked', 'booked'), ('shipped', 'shipped')], max_length=100, verbose_name='состояние'),
        ),
    ]
