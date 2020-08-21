fields = ['company-name', 'display-name', 'cnpj', 'city', 'state', 'cep', 'state-registration',
          'municipal-registration']


def correct_post(keys):
    sec_list = []

    for item in keys:
        if item in fields:
            sec_list.append(item)

    if len(sec_list) == len(fields):
        return True
    return False


def contains_a_valid_value():
    pass
