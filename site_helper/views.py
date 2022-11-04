from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from binance_get_price.models import PercentsCase, DataCase

names_bank = {
    'BCAMobile': 'BCA',
    'BankofGeorgia': 'Bank of Georgia (GEL)',
    'ForteBank': 'Forte Bank (KZT)',
    'KaspiBank': 'Kaspi Bank (KZT)',
    'LIBERTYBANK': 'Liberty Bank (GEL)',
    'PermataMe': ['Наличные на Бали', 'PERMATA'],
    'QIWI': 'QIWI (RUB)',
    'RosBankNew': 'Сбер (RUB)',
    'TBCbank': 'TBC Bank (GEL)',
    'TinkoffNew': 'Тинькофф (RUB)',
    'Uzcard': 'UZCARD (UZS)'
}


def delete_row(request):
    data_delete = {}
    for i in list(request.GET.keys()):
        if i != 'delete':
            if request.GET[i] != 'None':
                data_delete[i] = request.GET[i]
    print(data_delete)
    with transaction.atomic():
        try:
            PercentsCase.objects.filter(**data_delete).delete()
        except:
            pass


def update_or_create_row(request):
    data_update_or_create = {}
    defaults = {}
    for i in list(request.GET.keys()):
        if i != 'percent':
            if request.GET[i] != 'None':
                data_update_or_create[i] = request.GET[i]
        if request.GET[i] != 'None':
            defaults[i] = request.GET[i]
    with transaction.atomic():
        try:
            PercentsCase.objects.update_or_create(**data_update_or_create, defaults=defaults)
        except:
            pass


def index(request):
    list_keys = list(request.GET.keys())
    data_for_default = {}
    for i in list_keys:
        try:
            if request.GET[i] != 'None' and i != 'delete':
                data_for_default[i] = request.GET[i]
        except:
            data_for_default[i] = ''
    if 'delete' in list_keys:
        print('wef')
        delete_row(request)
    elif ('source_bank' in list_keys) and ('dest_bank' in list_keys) and (('min_price' in list_keys) or ('max_price' in list_keys)) and ('percent' in list_keys):
        update_or_create_row(request)
    data_to_search = []
    data = PercentsCase.objects.all()
    for i in DataCase.objects.all():
        for elem in [i.payment, i.asset]:
            key_list = False
            try:
                temp = names_bank[elem]
                try:
                    if type(temp) is list:
                        key_list = True
                except:
                    pass
            except:
                temp = elem
            if key_list:
                for j in temp:
                    if j not in data_to_search:
                        data_to_search.append(j)
            else:
                if temp not in data_to_search:
                    data_to_search.append(temp)
    data_to_search.sort(key=lambda x: x[0])
    return render(request, 'main/change_percents.html', {
        'title': 'Главная страница',
        'data_to_search': data_to_search,
        'data': data,
        'data_for_default': data_for_default
    })


# def detail(request):
#     try:
#         data_case = DataCase.objects.all()
#         data_case_texts = TextsCase.objects.all()
#         data_case = data_case.filter(ObjectID=request.GET['ObjectID'], type_of_legal_proceeding=request.GET['type_of_legal_proceeding'])
#         docx_base64 = ''
#         name_on_site = ''
#         name_doc = ''
#         date_doc = ''
#         try:
#             type_of_legal_proceeding = data_case[0].type_of_legal_proceeding
#             if type_of_legal_proceeding.find('Decision') != -1:
#                 type_of_legal_proceeding = type_of_legal_proceeding[:8] + 'Texts' + type_of_legal_proceeding[8:]
#                 print(type_of_legal_proceeding)
#                 data_case_texts = data_case_texts.filter(ObjectID=request.GET['ObjectID'], type_of_legal_proceeding=type_of_legal_proceeding)
#                 for one_data_case_texts in data_case_texts:
#                     if one_data_case_texts.PubAttach:
#                         docx_base64 = one_data_case_texts.PubAttach
#                         name_on_site = one_data_case_texts.FirstInstantDoc
#                         name_doc = one_data_case_texts.FirstInstantDecisioncText
#                         date_doc = one_data_case_texts.docdate
#                         break
#         except:
#             pass
#         key_judges = False
#         try:
#             if len(data_case[0].Judge.split(',')) > 1:
#                 key_judges = True
#         except:
#             pass
#         table_1 = ''
#         table_2 = ''
#         try:
#             if data_case[0].StateHistory:
#                 table_1 = data_case[0].StateHistory[:6] + ' id="table_1"' + data_case[0].StateHistory[6:]
#         except:
#             pass
#         try:
#             if data_case[0].HearingsCase:
#                 table_2 = data_case[0].HearingsCase[:6] + ' id="table_2"' + data_case[0].HearingsCase[6:]
#         except:
#             pass
#         return render(request, 'main/detail.html', {
#             'title': 'Детали по делу',
#             'data': data_case[0],
#             'docx_base64': docx_base64,
#             'name_on_site': name_on_site,
#             'name_doc': name_doc,
#             'date_doc': date_doc,
#             'key_judges': key_judges,
#             'table_1': table_1,
#             'table_2': table_2,
#         })
#     except:
#         return render(request, 'main/detail.html', {'title': 'Детали по делу', 'data': 'Bad'})



# def search(request):
#     # print(request.GET['Court'])
#     data_case = DataCase.objects.all()
#     # data_case2 = TextsCase.objects.all()
#     # a = []
#     # for i in data_case2:
#     #     a.append(i.ObjectID)
#     # for i in a:
#     #     if a.count(i) > 1:
#     #         print(i)
#     # print(len(a), len(list(set(a))))
#     key_for_accused = False
#     filters = {}
#     params = ''
#     if request.method == "GET":
#         list_keys = list(request.GET.keys())
#         print(list_keys)
#         for i in reversed(list_keys):
#             print(request.GET[i])
#             if request.GET[i].find('Не выбрано') != -1:
#                 list_keys.remove(i)
#         print(list_keys)
#         if 'Date' in list_keys:
#             filters['Date__year'] = request.GET['Date']
#             params += f'&Date={request.GET["Date"]}'
#         if ('type_of_legal_proceeding' not in list_keys) and ('ObjectID' not in list_keys):
#             detail_filters = const_type_of_legal_proceedings_sort['Административное']
#             temp_filter = Q(**{'type_of_legal_proceeding': detail_filters[0]})
#             for i in const_type_of_legal_proceedings_sort:
#                 for detail_filter in const_type_of_legal_proceedings_sort[i]:
#                     temp_filter.add(Q(**{'type_of_legal_proceeding': detail_filter}), Q.OR)
#             data_case = data_case.filter(temp_filter)
#             pass
#         for one_filter in ['ObjectID', 'Court', 'type_of_legal_proceeding', 'Judge', 'Name_people', 'Instance']:
#             key_add_params = True
#             if one_filter in list_keys:
#                 # print(request.GET[one_filter])
#                 if request.GET[one_filter]:
#                     if request.GET[one_filter].find('Не выбрано') != -1:
#                         continue
#                     if one_filter == 'type_of_legal_proceeding':
#                         if request.GET[one_filter] == 'Уголовное':
#                             key_for_accused = True
#                         try:
#                             if (request.GET['Court'] == 'Верховный суд') and ('Instance' in list_keys):
#                                 key_type_of_legal_proceeding = False
#                             else:
#                                 key_type_of_legal_proceeding = True
#                         except:
#                             key_type_of_legal_proceeding = True
#                         if key_type_of_legal_proceeding:
#                             detail_filters = const_type_of_legal_proceedings_sort[request.GET[one_filter]]
#                             temp_filter = Q(**{one_filter: detail_filters[0]})
#                             for detail_filter in detail_filters[1:]:
#                                 temp_filter.add(Q(**{one_filter: detail_filter}), Q.OR)
#                             data_case = data_case.filter(temp_filter)
#                     elif one_filter == 'Court':
#                         filters[f'{one_filter}'] = const_courts_short[request.GET[one_filter]]
#                     elif one_filter == 'Judge':
#                         full_name = sort_full_name(request, one_filter)
#                         # filters[f'{one_filter}__icontains'] = full_name
#                         temp_filter = Q(**{f'{one_filter}__icontains': full_name})
#                         for name_judge in ['PresidingJudge', 'JudgeSpeaker', 'ThirdJudge', 'FourthJudge', 'FifthJudge']:
#                             temp_filter.add(Q(**{f'{name_judge}__icontains': full_name}), Q.OR)
#                         data_case = data_case.filter(temp_filter)
#                     elif one_filter == 'Name_people':
#                         temp_filter = Q(**{'Plaintiff__icontains': request.GET[one_filter]})
#                         temp_filter.add(Q(**{'Defendant__icontains': request.GET[one_filter]}), Q.OR)
#                         data_case = data_case.filter(temp_filter)
#                     elif one_filter == 'Instance':
#                         if request.GET[one_filter] == 'Первая' or request.GET[one_filter] == 'Кассационная':
#                             if request.GET[one_filter] == 'Кассационная':
#                                 if 'Court' not in list_keys:
#                                     filters[f'Court'] = const_courts_short['Верховный суд']
#                             if 'type_of_legal_proceeding' in list_keys:
#                                 temp_filter = const_type_of_legal_proceedings_sort[
#                                     request.GET['type_of_legal_proceeding']]
#                                 list_instance = []
#                                 for i in temp_filter:
#                                     if i in const_instances_short[request.GET[one_filter]]:
#                                         list_instance.append(i)
#                             else:
#                                 list_instance = const_instances_short[request.GET[one_filter]]
#                             temp_filter = Q(**{'type_of_legal_proceeding': list_instance[0]})
#                             for detail_instance in list_instance[1:]:
#                                 temp_filter.add(Q(**{'type_of_legal_proceeding': detail_instance}), Q.OR)
#                             data_case = data_case.filter(temp_filter)
#                         if request.GET[one_filter] == 'Надзорная':
#                             if 'ObjectID' not in list_keys:
#                                 filters[f'Court'] = '3yru3vyuuyv3r'
#                             pass
#                     elif one_filter == 'ObjectID':
#                         temp_filter = Q(**{'ObjectID': request.GET[one_filter]})
#                         temp_filter.add(Q(**{'StringNumber__startswith': request.GET[one_filter]}), Q.OR)
#                         data_case = data_case.filter(temp_filter)
#                         # filters[f'{one_filter}__icontains'] = request.GET[one_filter]
#                     if key_add_params:
#                         params += f'&{one_filter}={request.GET[one_filter]}'
#         # print(filters)
#         # print(params)
#         data_for_default = {}
#         for i in ['Court', 'Instance', 'type_of_legal_proceeding', 'ObjectID', 'Judge', 'Date', 'Name_people', 'Instance']:
#             try:
#                 if request.GET[i].find('Не выбрано') != -1:
#                     continue
#                 data_for_default[i] = request.GET[i]
#             except:
#                 data_for_default[i] = ''
#         data_case = data_case.filter(**filters)
#         if params:
#             params = params
#         context = {
#             "title": "Поиск по судебным делам",
#             "courts": ['Не выбрано '] + const_courts,
#             "instances": ['Не выбрано  '] + const_instances,
#             "type_of_legal_proceedings": ['Не выбрано   '] + const_type_of_legal_proceedings,
#             "judges": ['Не выбрано    '] + const_judges,
#             "years": ['Не выбрано     '] + const_years,
#             "page_obj": page_split(data_case, request),
#             "params": params,
#             "count_cases": len(data_case),
#             "key_for_accused": key_for_accused,
#             "data_for_default": data_for_default,
#         }
#         return render(request, 'main/search.html', context)
