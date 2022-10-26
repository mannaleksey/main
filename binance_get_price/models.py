from django.db import models


class DataCase(models.Model):
    trade_type = models.CharField('Купить-Продать', max_length=64)
    payment = models.CharField('Банк', max_length=64)
    price = models.CharField('Цена', max_length=64)

    def __str__(self):
        return self.payment

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
