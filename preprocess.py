def address_preprocessing(address):
    address = address.replace('ул.', 'улица')
    address = address.replace('ул,', 'улица')
    address = address.replace('ул ', 'улица ')
    address = address.replace('вл ', '')
    address = address.replace('вл', '')
    address = address.replace('пер ', 'переулок')
    address = address.replace('пер.', 'переулок')
    address = address.replace('наб ', 'набережная ')
    address = address.replace('наб.', 'набережная')
    address = address.replace('пр-кт', 'проспект')
    address = address.replace('ш.', 'шоссе')
    address = address.replace('ш ', 'шоссе')
    address = address.replace('б-р', 'бульвар')
    address = address.replace('бул', 'бульвар')
    address = address.replace('корп.', 'к')
    address = address.replace('корп ', 'к')
    address = address.replace('корп', 'к')
    address = address.replace('к.', 'к')
    address = address.replace('стр', 'с')
    address = address.replace('стр.', 'с')
    address = address.replace('с.', 'с')
    address = address.replace('м. ', '')

    for j in range(len(address)):
        try:
            if (address[j] == 'к' or address[j] == 'К') and address[j + 1].isdigit():
                address = address[:j]
                break
            if (address[j] == 'К' or address[j] == 'к') and address[j + 1] == " " and address[j + 2].isdigit():
                address = address[:j]
                break

            if (address[j] == 'с' or address[j] == 'С') and address[j + 1].isdigit():
                address = address[:j]
                break
            if (address[j] == 'с' or address[j] == 'С') and address[j + 1] == " " and address[j + 2].isdigit():
                address = address[:j]
                break
        except Exception as E:
            pass
    address = address.replace(',', '')
    address = address.replace('.', '')
    address = ' '.join(address.split())
    return address


def preprocess_metro(metro):
    metro = metro.replace(' (КРЛ)', '')
    metro = metro.replace(' (БКЛ)', '')
    metro = metro.replace(' (КЛ)', '')
    metro = metro.replace(' (ФЛ)', '')
    metro = metro.replace(' (ФЛ)', '')
    metro = metro.replace(' (МНР)', '')
    metro = metro.replace(' (ЗМЛ)', '')
    return metro
