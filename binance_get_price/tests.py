from pprint import pprint

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
    'PERMATA': 'PermataMe',
    'BCA': 'BCAMobile',
    'Наличные на Бали': 'PermataMe',
    # 'abc2': 'PermataMe'
}

a = {}
for key, value in names_bank.items():
    a[value] = key
pprint(a, indent=4)
