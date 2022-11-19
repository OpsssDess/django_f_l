import uuid

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.db.models import Sum
from django.db.models import Q, F

class CompletedRequestManager(models.Model):
    def get_queryset(self):
        return super().get_queryset().filter(status='satisfied')

class Thing(models.Model):
    name = models.CharField(max_length=50, verbose_name='имя вещи')
    type_thing = models.CharField(max_length=255, verbose_name='тип вещи')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)

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

    def __str__(self):
        return self.name_strategy


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


class BaseItem(models.Model):
    base_item_hash = models.ForeignKey('Thing', db_column='base_item_hash', on_delete=models.CASCADE)
    office = models.ForeignKey('Office', on_delete=models.CASCADE, verbose_name='склад')


class DonationItem(BaseItem):
    state = models.CharField(max_length=250)
    donation = models.ForeignKey('Donation', on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

@receiver(signals.post_save, sender=DonationItem)
def counting_places(sender, instance, **kwargs):
    all_goods = DonationItem.objects.filter(office=instance.office.pk)
    count = 0
    for i in all_goods:
        count += i.amount
    # amount_all_goods = all_goods.aggregate(sum_amount=Sum('amount'))
    actual_stock = Office.objects.get(pk=instance.office.pk)
    actual_stock.ocupied = count
    actual_stock.save()


class RequestItem(BaseItem):
    request = models.ForeignKey('HelpRequest', on_delete=models.CASCADE)
    amount_item = models.IntegerField(default=1)


class ItemDescription(DonationItem):
    details = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    condition = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True)


class Collection(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    donation_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.creation_date)

class Donation(Collection):
    CHOICES = (
        ('available', 'available'),
        ('booked', 'booked'),
    )
    status_donation = models.CharField(max_length=250, choices=CHOICES, default='available', blank=True)


class HelpRequest(Collection):
    CHOICES = (
        ('satisfied', 'satisfied'),
        ('unsatisfied', 'unsatisfied'),
    )
    status_help_request = models.CharField(max_length=250, choices=CHOICES, default='unsatisfied', blank=True)


class CompletedRequest(HelpRequest):
    class Meta:
        proxy = True

    object = CompletedRequestManager()







# class ItemMedia(models.Model):
#     title = models.CharField(max_length=250)
#     file = models.FileField(upload_to='files')
#     type = models.CharField(max_length=250)
#     preview = models.CharField(max_length=250)
#     status = models.CharField(max_length=250, choices=STATUS, verbose_name='состояние')



