from django.db import models

class Good(models.Model):
    name_good = models.CharField(max_length=50)
    amount = models.IntegerField()

    def __str__(self):
        return self.name_good