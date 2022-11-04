# Generated by Django 4.1.2 on 2022-11-04 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.CharField(default='', max_length=64, verbose_name='Криптовалюта')),
                ('trade_type', models.CharField(default='', max_length=64, verbose_name='Купить-Продать')),
                ('payment', models.CharField(default='', max_length=64, verbose_name='Банк')),
                ('price', models.CharField(default='', max_length=64, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='PercentsCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_bank', models.CharField(default='', max_length=64, verbose_name='Банк (от куда)')),
                ('dest_bank', models.CharField(default='', max_length=64, verbose_name='Банк (куда)')),
                ('percent', models.DecimalField(decimal_places=5, default='', max_digits=10, verbose_name='Процент')),
                ('min_price', models.DecimalField(decimal_places=5, default='', max_digits=10, verbose_name='Макс цена')),
                ('max_price', models.DecimalField(decimal_places=5, default='', max_digits=10, verbose_name='Мин цена')),
            ],
            options={
                'verbose_name': 'Процент',
                'verbose_name_plural': 'Проценты',
            },
        ),
        migrations.CreateModel(
            name='SpotCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_coin', models.CharField(default='', max_length=64, verbose_name='Монета (от куда)')),
                ('dest_coin', models.CharField(default='', max_length=64, verbose_name='Монета (куда)')),
                ('price', models.DecimalField(decimal_places=5, default='', max_digits=10, verbose_name='Процент')),
            ],
            options={
                'verbose_name': 'Курс монеты',
                'verbose_name_plural': 'Курсы монет',
            },
        ),
    ]
