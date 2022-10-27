from django.db import models


class DataCase(models.Model):
    trade_type = models.CharField('Купить-Продать', max_length=64)
    payment = models.CharField('Банк', max_length=64)
    price = models.CharField('Цена', max_length=64)

    def __str__(self):
        return f'{self.trade_type} - {self.payment} - {self.price}'

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class PercentsCase(models.Model):
    source_bank = models.CharField('Банк (от куда)', max_length=64)
    dest_bank = models.CharField('Банк (куда)', max_length=64)
    percent = models.DecimalField('Проецт', max_digits=10, decimal_places=5)

    def __str__(self):
        return f'{self.source_bank} - {self.dest_bank} - {self.percent}'

    class Meta:
        verbose_name = "Процент"
        verbose_name_plural = "Проценты"
