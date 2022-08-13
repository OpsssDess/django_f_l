from django.db import models

class Good(models.Model):
    thing = models.CharField(max_length=50, verbose_name='вещь')
    amount = models.IntegerField(verbose_name='количество')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    stock = models.CharField(max_length=50, verbose_name='тип сортировки')
    state = models.CharField(max_length=100, verbose_name='состояние')
    office = models.ForeignKey('Office', on_delete=models.CASCADE, verbose_name='склад')

    def __str__(self):
        return self.thing

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи которые принесли'
        ordering = ['-stock', '-time_create']

class Office(models.Model):
    address = models.CharField(max_length=250, verbose_name='склад')
    capacity = models.IntegerField(verbose_name='вместимость')
    ocupied = models.IntegerField(verbose_name='заполненость')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'склад'
        verbose_name_plural = 'склады'
        ordering = ['ocupied']