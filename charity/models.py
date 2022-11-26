import uuid

from PIL import Image
from django.contrib.auth.models import User
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
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

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

    def __str__(self):
        return self.base_item_hash.name

class DonationItem(BaseItem):
    state = models.CharField(max_length=250)
    donation = models.ForeignKey('Donation', on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

@receiver(signals.post_save, sender=DonationItem)
def counting_places(sender, instance, **kwargs):
    all_goods = DonationItem.objects.filter(office=instance.office.pk)
    amount_all_goods = all_goods.aggregate(sum_amount=Sum('amount'))
    actual_stock = Office.objects.get(pk=instance.office.pk)
    actual_stock.ocupied = amount_all_goods['sum_amount']
    actual_stock.save()



class RequestItem(BaseItem):
    request = models.ForeignKey('HelpRequest', on_delete=models.CASCADE)
    amount_req_item = models.IntegerField(default=1)

@receiver(signals.post_save, sender=RequestItem)
def change_status(sender, instance, **kwargs):
    need_good = instance.base_item_hash
    try:
        need_don_item = DonationItem.objects.get(base_item_hash__exact=need_good)
        if need_don_item.amount > instance.amount_req_item:
            need_don_item.amount -= instance.amount_req_item
            need_don_item.save()
            need_don_item.donation.status_donation = 'used'
            need_don_item.donation.save()

        elif need_don_item.amount == instance.amount_req_item:
            need_don_item.amount = 0
            need_don_item.save()
            need_don_item.donation.status_donation = 'booked'
            need_don_item.donation.save()
        instance.request.status_help_request = 'satisfied'
        instance.request.save()

    except DonationItem.DoesNotExist:
        instance.request.status_help_request = 'waiting'
        instance.request.save()


class ItemDescription(DonationItem):
    details = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    condition = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)

    @property
    def get_img_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/media/images/ball.jpeg"

    def save(self, *args, **kwargs):
        super(ItemDescription, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 100 or img.width > 100:
                img.thumbnail((100, 100))
                img.save(self.image.path)




class Collection(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    donation_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

class Donation(Collection):
    CHOICES = (
        ('available', 'available'),
        ('booked', 'booked'),
        ('used', 'used'),
    )
    status_donation = models.CharField(max_length=250, choices=CHOICES, default='available', blank=True)


class HelpRequest(Collection):
    CHOICES = (
        ('satisfied', 'satisfied'),
        ('unsatisfied', 'unsatisfied'),
        ('waiting', 'waiting'),
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



