from decimal import Decimal

from django.db import models


class DataCase(models.Model):
    asset = models.CharField('Криптовалюта', max_length=64, default='')
    trade_type = models.CharField('Купить-Продать', max_length=64, default='')
    payment = models.CharField('Банк', max_length=64, default='')
    price = models.CharField('Цена', max_length=64, default='')

    def __str__(self):
        return f'{self.asset} - {self.trade_type} - {self.payment} - {self.price}'

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class PercentsCase(models.Model):
    source_bank = models.CharField('Банк (от куда)', max_length=64, default='')
    dest_bank = models.CharField('Банк (куда)', max_length=64, default='')
    percent = models.DecimalField('Процент', max_digits=10, decimal_places=5, null=True)
    min_price = models.DecimalField('Макс цена', max_digits=20, decimal_places=5, null=True)
    max_price = models.DecimalField('Мин цена', max_digits=20, decimal_places=5, null=True)

    def __str__(self):
        return f'{self.source_bank} - {self.dest_bank} - {self.percent} ({self.min_price} - {self.max_price})'

    class Meta:
        verbose_name = "Процент"
        verbose_name_plural = "Проценты"


class SpotCase(models.Model):
    source_coin = models.CharField('Монета (от куда)', max_length=64, default='')
    dest_coin = models.CharField('Монета (куда)', max_length=64, default='')
    price = models.DecimalField('Процент', max_digits=20, decimal_places=5, null=True)

    def __str__(self):
        return f'{self.source_coin} - {self.dest_coin} - {self.price}'

    class Meta:
        verbose_name = "Курс монеты"
        verbose_name_plural = "Курсы монет"
