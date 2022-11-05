from decimal import Decimal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DataCase, PercentsCase

names_bank = {
    'Сбер (RUB)': 'RosBankNew',
    'Тинькофф (RUB)': 'TinkoffNew',
    'QIWI (RUB)': 'QIWI',
    'Kaspi Bank (KZT)': 'KaspiBank',
    'Forte Bank (KZT)': 'ForteBank',
    'Bank of Georgia (GEL)': 'BankofGeorgia',
    'TBC Bank (GEL)': 'TBCbank',
    'Liberty Bank (GEL)': 'LIBERTYBANK',
    'UZCARD (UZS)': 'Uzcard',
    'Permata Bank (IDR)': 'PermataMe',
    'BCA (IDR)': 'BCAMobile',
    'Наличные на Бали': 'PermataMe',
    # 'abc2': 'PermataMe'
}


def get_course(asset, trade_type, payment):
    payment = names_bank[payment]
    data_case = DataCase.objects.all()
    return Decimal(data_case.filter(asset=asset, trade_type=trade_type, payment=payment)[0].price)


@api_view(['GET'])
def get_cost(request):
    data = {'result': '0'}
    keys_list = list(request.GET.keys())
    try:
        if ('source' in keys_list) and ('dest' in keys_list) and ('price' in keys_list):
            if request.GET['source'] not in ['BTC', 'ETH', 'USDT'] and request.GET['dest'] not in ['BTC', 'ETH', 'USDT']:
                source_course = get_course('USDT', 'BUY', request.GET['source'])
                dest_course = get_course('USDT', 'SELL', request.GET['dest'])
                if source_course and dest_course:
                    data['result'] = str(Decimal(request.GET['price']) / source_course * dest_course)
            elif request.GET['source'] in ['BTC', 'ETH', 'USDT'] and request.GET['dest'] not in ['BTC', 'ETH', 'USDT']:
                dest_course = get_course(request.GET['source'], 'SELL', request.GET['dest'])
                if dest_course:
                    data['result'] = str(Decimal(request.GET['price']) * dest_course)
            try:
                if data['result'] != '0':
                    list_elem = PercentsCase.objects.all().filter(source_bank=request.GET['source'], dest_bank=request.GET['dest'])
                    for elem in list_elem:
                        if elem.min_price and elem.max_price:
                            if elem.min_price <= Decimal(request.GET['price']) < elem.max_price:
                                percent = elem.percent / Decimal('100') + Decimal('1')
                                data['result'] = str(Decimal(data['result']) * percent)
                                break
                        elif elem.min_price and not elem.max_price:
                            if elem.min_price <= Decimal(request.GET['price']):
                                percent = elem.percent / Decimal('100') + Decimal('1')
                                data['result'] = str(Decimal(data['result']) * percent)
                                break
                        elif not elem.min_price and elem.max_price:
                            if Decimal(request.GET['price']) < elem.max_price:
                                percent = elem.percent / Decimal('100') + Decimal('1')
                                data['result'] = str(Decimal(data['result']) * percent)
                                break
            except:
                pass
        else:
            pass
    except:
        pass
    return Response(data)
