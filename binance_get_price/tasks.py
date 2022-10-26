import time
from celery import shared_task
from django.db import transaction
from .models import DataCase
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
import requests

headers = {
    'clienttype': 'android',
    'lang': 'vi',
    'versioncode': '14004',
    'versionname': '1.40.4',
    'BNC-App-Mode': 'pro',
    'BNC-Time-Zone': 'Asia/Ho_Chi_Minh',
    'BNC-App-Channel': 'play',
    'BNC-UUID': '067042cf79631252f1409a9baf052e1a',
    'referer': 'https://www.binance.com/',
    'Cache-Control': 'no-cache, no-store',
    'Content-Type': 'application/json',
    'X-MBX-APIKEY': 'UeokiKzPh0evwMSo5p3P6GaCyttA7jFEVMNodmDYLQlMCHpJ7sd24NkPq529yUZk',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'okhttp/4.9.0'
}


def load_data(data):
    with transaction.atomic():
        for trade_type, payment, price in data:
            try:
                obj, created = DataCase.objects.update_or_create(
                    trade_type=trade_type,
                    payment=payment,
                    defaults={
                        'trade_type': trade_type,
                        'payment': payment,
                        'price': price,
                    }
                )
            except:
                pass


def get_cost(data_input):
    trade_type, payment, fiat = data_input
    asset = 'USDT'
    for num_page in range(1, 10):
        try:
            response = requests.post(
                url='https://www.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
                headers=headers,
                json={
                    'asset': asset,
                    'tradeType': f'{trade_type}',
                    'fiat': f'{fiat}',
                    'page': f'{num_page}',
                    'payTypes': [payment],
                    'rows': '10',
                }
            )
            response_json = response.json()['data']
            if num_page == 1:
                response_json = response_json[3:]
            for order in response_json:
                min_price_usdt = Decimal(order['adv']['minSingleTransQuantity'])
                if Decimal(min_price_usdt) > Decimal('100'):
                    return [trade_type, payment, str(round(Decimal(order['adv']['price']), 5))]
        except:
            pass


def main():
    data_all_input = [
        ['BUY', 'RosBankNew', 'RUB'], ['BUY', 'TinkoffNew', 'RUB'], ['BUY', 'QIWI', 'RUB'],
        ['SELL', 'KaspiBank', 'KZT'], ['SELL', 'ForteBank', 'KZT'],
        ['SELL', 'BankofGeorgia', 'GEL'], ['SELL', 'TBCbank', 'GEL'], ['SELL', 'LIBERTYBANK', 'GEL'],
        ['SELL', 'Uzcard', 'UZS'],
        ['SELL', 'PermataMe', 'IDR'],
    ]
    with ThreadPoolExecutor() as executor:
        # data = list(tqdm(executor.map(get_results, list_all_items), total=len(list_all_items)))
        data = list(executor.map(get_cost, data_all_input))
    load_data(data)


@shared_task
def refresh_db():
    start_time = time.time()
    try:
        main()
    except:
        pass
    print(time.time() - start_time)
