from django.db import models

class Good(models.Model):
    name_good = models.CharField(max_length=50)
    amount = models.IntegerField()
    time_create = models.DateTimeField(auto_now_add=True)
    stock = models.CharField(max_length=50)

    def __str__(self):
        return self.name_good