import random
import uuid
import urllib3
import base64
import json


def create_random_client(
        path: str = 'api/client/',
        url_base: str = 'http://localhost:8000',
        user_api: str = 'api',
        passwd_api: str = 'api') -> bool:
    base64auth = '%s:%s' % (user_api, passwd_api)

    http = urllib3.PoolManager()

    uid = str(uuid.uuid4()).split('-')[1]
    body_data = {
        "company_name": "company_%s" % uid,
        "display_name": "Company %s" % uid,
        "cnpj": "93.400.255/0001-22",
        "city": "58415-528",
        "state": "PB",
        "cep": " 58415-528",
        "district": "Cruzeiro",
        "address": " Rua Hermínio Monteiro",
        "state_registration": "ISENTO",
        "municipal_registration": "ISENTO",
        "logo": None,
        "user": None,
        "mail": "company_%s@company_%s.org" %  (uid, uid)
    }

    req = http.request(
        'POST',
        '%s/%s' % (url_base, path),
        body=json.dumps(body_data).encode('utf-8'),
        headers={
            'Authorization': 'Basic %s' % base64.b64encode(base64auth.encode("utf-8")).decode('utf-8'),
            'Content-Type': 'application/json'
        }
    )

    response = json.loads(req.data.decode('utf-8'))

    if not 'id' in response:
        return False

    return True

if __name__ == '__main__':
    if create_random_client():
        print('✅ Criação de clientes funcionando...')
    else:
        print('❌ Ops... Criação de clientes apresenta falha...')
