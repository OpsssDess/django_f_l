# Generated by Django 4.0.6 on 2022-10-16 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0007_alter_good_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='stock',
            field=models.CharField(choices=[('LIFO', 'LIFO'), ('FIFO', 'FIFO')], max_length=50, verbose_name='тип сортировки'),
        ),
    ]