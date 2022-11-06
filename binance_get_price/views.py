from decimal import Decimal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DataCase, PercentsCase, NameCase


def get_back_name_cripto(front_name_cripto):
    try:
        back_name_cripto = NameCase.objects.all().filter(front_name=front_name_cripto)[0].back_name
        return back_name_cripto
    except:
        return front_name_cripto


def get_course(asset, trade_type, payment):
    try:
        payment = NameCase.objects.all().filter(front_name=payment)[0].back_name
        return Decimal(DataCase.objects.all().filter(asset=asset, trade_type=trade_type, payment=payment)[0].price)
    except:
        pass


@api_view(['GET'])
def get_cost(request):
    data = {'result': '0'}
    keys_list = list(request.GET.keys())
    try:
        if ('source' in keys_list) and ('dest' in keys_list) and ('price' in keys_list):
            cripto_front_name_list = []
            for cripto in ['BTC', 'ETH', 'USDT']:
                try:
                    cripto_front_name_list.append(NameCase.objects.all().filter(back_name=cripto)[0].front_name)
                except:
                    cripto_front_name_list.append(cripto)
            if request.GET['source'] not in cripto_front_name_list and request.GET['dest'] not in cripto_front_name_list:
                source_course = get_course('USDT', 'BUY', request.GET['source'])
                dest_course = get_course('USDT', 'SELL', request.GET['dest'])
                if source_course and dest_course:
                    data['result'] = str(Decimal(request.GET['price']) / source_course * dest_course)
            elif request.GET['source'] in cripto_front_name_list and request.GET['dest'] not in cripto_front_name_list:
                dest_course = get_course(get_back_name_cripto(request.GET['source']), 'SELL', request.GET['dest'])
                if dest_course:
                    data['result'] = str(Decimal(request.GET['price']) * dest_course)
            elif request.GET['source'] not in cripto_front_name_list and request.GET['dest'] in cripto_front_name_list:
                dest_course = get_course(get_back_name_cripto(request.GET['dest']), 'BUY', request.GET['source'])
                if dest_course:
                    data['result'] = str(Decimal(request.GET['price']) / dest_course)
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
