from decimal import Decimal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DataCase, PercentsCase

names_bank = {
    'Сбер (RUB)': 'RosBankNew',
    # 'abc1': 'RosBankNew',
    'Тинькофф (RUB)': 'TinkoffNew',
    'QIWI (RUB)': 'QIWI',
    'Kaspi Bank (KZT)': 'KaspiBank',
    'Forte Bank (KZT)': 'ForteBank',
    'Bank of Georgia (GEL)': 'BankofGeorgia',
    'TBC Bank (GEL)': 'TBCbank',
    ' Liberty Bank (GEL)': 'LIBERTYBANK',
    'UZCARD (UZS)': 'Uzcard',
    'Индонезия (IDR)': 'PermataMe'
    # 'abc2': 'PermataMe'
}


def get_course(trade_type, payment):
    payment = names_bank[payment]
    data_case = DataCase.objects.all()
    return Decimal(data_case.filter(trade_type=trade_type, payment=payment)[0].price)


@api_view(['GET'])
def get_cost(request):
    data = {}
    keys_list = list(request.GET.keys())
    try:
        if ('source' in keys_list) and ('dest' in keys_list) and ('price' in keys_list):
            if 'source' in keys_list:
                source_course = get_course('BUY', request.GET['source'])
            if 'dest' in keys_list:
                dest_course = get_course('SELL', request.GET['dest'])
            if source_course and dest_course:
                try:
                    percent = PercentsCase.objects.all().filter(source_bank=request.GET['source'], dest_bank=request.GET['dest'])[0].percent / Decimal('100') + Decimal('1')
                except:
                    percent = Decimal('1')
                data['result'] = str(round(Decimal(request.GET['price']) / source_course * dest_course, 2) * percent)
        else:
            data['result'] = '0'
    except:
        data['result'] = '0'
    return Response(data)
