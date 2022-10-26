from decimal import Decimal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DataCase


def get_course(trade_type, payment):
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
                data['result'] = str(round(Decimal(request.GET['price']) / source_course * dest_course, 2))
        else:
            data['result'] = '0'
    except:
        data['result'] = '0'
    return Response(data)
