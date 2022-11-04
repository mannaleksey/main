import time
from celery import shared_task
from django.db import transaction
try:
    from .models import DataCase, SpotCase
except:
    pass
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

ALL_BANKS = [
    ['RosBankNew', 'RUB'], ['TinkoffNew', 'RUB'], ['QIWI', 'RUB'],
    ['KaspiBank', 'KZT'], ['ForteBank', 'KZT'],
    ['BankofGeorgia', 'GEL'], ['TBCbank', 'GEL'], ['LIBERTYBANK', 'GEL'],
    ['Uzcard', 'UZS'],
    ['PermataMe', 'IDR'], ['BCAMobile', 'IDR'],
]
ALL_CRIPTO = ['USDT', 'BTC', 'ETH']


def spot(symbol):
    result = []
    while True:
        try:
            response = requests.get(
                url='https://www.binance.com/api/v3/ticker/24hr',
                headers=headers,
                params={
                    'symbol': symbol[0] + symbol[1]
                }
            )
            price = Decimal(response.json()['bidPrice'].replace(',', ''))
            with transaction.atomic():
                try:
                    SpotCase.objects.update_or_create(
                        source_coin=symbol[0],
                        dest_coin=symbol[1],
                        defaults={
                            'source_coin': symbol[0],
                            'dest_coin': symbol[1],
                            'price': price,
                        }
                    )
                except:
                    pass
            break
        except:
            return None
            pass
    return result


def load_data(data):
    with transaction.atomic():
        # for asset, trade_type, payment, price in data:
        asset, trade_type, payment, price = data
        try:
            DataCase.objects.update_or_create(
                asset=asset,
                trade_type=trade_type,
                payment=payment,
                defaults={
                    'asset': asset,
                    'trade_type': trade_type,
                    'payment': payment,
                    'price': price,
                }
            )
        except:
            pass


def get_cost(data_input):
    asset, trade_type, payment, fiat = data_input
    if asset == 'USDT':
        equal_usdt = '100'
    else:
        try:
            equal_usdt = Decimal("100") / SpotCase.objects.all().filter(source_coin=asset, dest_coin='USDT')[0].price
        except:
            return [asset, trade_type, payment, str(0)]
    for num_page in range(1, 10):
        try:
            response = requests.post(
                url='https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
                headers=headers,
                json={
                    'asset': asset,
                    'tradeType': f'{trade_type}',
                    'fiat': f'{fiat}',
                    'page': f'{num_page}',
                    'payTypes': [payment],
                    'rows': '20',
                }
            )
            if response.text == '':
                print(f'bad {[asset, trade_type, payment]}')
            response_json = response.json()['data']
            if num_page == 1:
                response_json = response_json[3:]
            for order in response_json:
                min_price_usdt = Decimal(order['adv']['minSingleTransQuantity'])
                if Decimal(min_price_usdt) > Decimal(equal_usdt):
                    return [asset, trade_type, payment, str(round(Decimal(order['adv']['price']), 5))]
        except:
            pass
    return [asset, trade_type, payment, str(0)]


def main():
    for symbol in [['BTC', 'USDT'], ['ETH', 'USDT']]:
        spot(symbol)
    data_all_input = []
    for bank_fiat in ALL_BANKS:
        for trade_type in ['BUY', 'SELL']:
            for asset in ALL_CRIPTO:
                data_all_input.append([asset, trade_type] + bank_fiat)
    for i in data_all_input:
        data = get_cost(i)
        load_data(data)
        time.sleep(5)
    # with ThreadPoolExecutor() as executor:
    #     # data = list(tqdm(executor.map(get_results, list_all_items), total=len(list_all_items)))
    #     data = list(executor.map(get_cost, data_all_input))
    # print(data)


@shared_task
def refresh_db():
    start_time = time.time()
    try:
        main()
    except:
        pass
    print(time.time() - start_time)


if __name__ == '__main__':
    while True:
        main()
