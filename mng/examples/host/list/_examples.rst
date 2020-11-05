.. code-block::bash

    mng host list

.. output::

    [ { 'arch': 'AMD64',
        'cores': 4,
        'environment': 1,
        'equipment': 'real',
        'frequency': 2201.0,
        'hostname': 'DESKTOP-VQDVFV4',
        'id': 4,
        'instances': [ { 'database': '',
                         'id': 1,
                         'private_ip': '10.0.10.5',
                         'service': { 'dns': 'postgres.intranet.com',
                                      'id': 1,
                                      'name': 'PostgresSQL',
                                      'port': 321}},
                       { 'database': '',
                         'id': 2,
                         'private_ip': '10.0.10.20',
                         'service': None}],
        'os_name': 'nt',
        'platform': 'Windows-10-10.0.18362-SP0',
        'processor': 'Intel64 Family 6 Model 61 Stepping 4, '
                     'GenuineIntel',
        'ram': 8.0}]