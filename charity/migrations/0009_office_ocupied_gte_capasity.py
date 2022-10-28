# Generated by Django 4.0.6 on 2022-10-19 20:38

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0008_alter_good_stock'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='office',
            constraint=models.CheckConstraint(check=models.Q(('ocupied__lte', django.db.models.expressions.F('capacity'))), name='ocupied_gte_capasity'),
        ),
    ]
