import uuid

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.db.models import Sum
from django.db.models import Q, F


class Thing(models.Model):
    name = models.CharField(max_length=50, verbose_name='имя вещи')
    type_thing = models.CharField(max_length=255, verbose_name='тип вещи')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'


class Category(models.Model):
    CHOICES_STRATEGY = (
        ('LIFO', 'LIFO'),
        ('FIFO', 'FIFO')
    )
    name_strategy = models.CharField(max_length=50, choices=CHOICES_STRATEGY)


class Office(models.Model):
    address = models.CharField(max_length=250, verbose_name='склад')
    capacity = models.IntegerField(verbose_name='вместимость')
    ocupied = models.IntegerField(verbose_name='заполненость')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'склад'
        verbose_name_plural = 'склады'
        constraints = [
            models.CheckConstraint(check=models.Q(ocupied__lte=F('capacity')), name='ocupied_lte_capasity'),
        ]
# cигнал с прошлой домашней работы
# @receiver(signals.post_save, sender=Thing)
# def counting_places(sender, instance, **kwargs):
#     all_goods = Thing.objects.filter(office=instance.office).exclude(state='shipped')
#     amount_all_goods = all_goods.aggregate(sum_amount=Sum('amount'))
#     actual_stock = Office.objects.get(address=instance.office)
#     actual_stock.ocupied = amount_all_goods['sum_amount']
#     actual_stock.save()


class BaseItem(models.Model):
    base_item_hash = models.ForeignKey('Thing', db_column='base_item_hash', on_delete=models.CASCADE)
    office = models.ForeignKey('Office', on_delete=models.CASCADE, verbose_name='склад')


class RequestItem(BaseItem):
    request = models.ForeignKey('HelpRequest', on_delete=models.CASCADE)
    donation_item = models.ForeignKey('DonationItem', on_delete=models.CASCADE)


class DonationItem(BaseItem):
    state = models.CharField(max_length=250)
    donation = models.ForeignKey('Donation', on_delete=models.CASCADE)

class ItemDescription(DonationItem):
    details = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    condition = models.CharField(max_length=250)
    item_hash = models.ForeignKey('Thing', db_column='item_description_hash', on_delete=models.CASCADE)


class Collection(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    donation_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

class Donation(Collection):
    pass

class HelpRequest(Collection):
    pass

class CompletedRequest(HelpRequest):
    class Meta:
        proxy = True







# class ItemMedia(models.Model):
#     STATUS = (
#         ('requested', 'requested'),
#         ('available', 'available'),
#         ('booked', 'booked'),
#         ('shipped', 'shipped'),
#     )
#     title = models.CharField(max_length=250)
#     file = models.FileField(upload_to='files')
#     type = models.CharField(max_length=250)
#     preview = models.CharField(max_length=250)
#     status = models.CharField(max_length=250, choices=STATUS, verbose_name='состояние')



