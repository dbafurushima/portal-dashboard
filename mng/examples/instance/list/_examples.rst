.. code-block::bash

    mng instance list

output::

    [ { 'database': '',
	    'host': { 'arch': 'AMD64',
                  'cores': 4,
                  'environment': 1,
                  'equipment': 'real',
                  'frequency': 2201.0,
                  'hostname': 'DESKTOP-VQDVFV4',
                  'id': 4,
                  'os_name': 'nt',
                  'platform': 'Windows-10-10.0.18362-SP0',
                  'private_ip': '192.168.1.4',
                  'processor': 'Intel64 Family 6 Model 61 '
                               'Stepping 4, GenuineIntel',
                  'public_ip': '45.234.102.90',
                  'ram': 8.0},
        'id': 1,
        'name': 'VM0',
        'private_ip': '10.0.10.5',
        'service': { 'dns': 'postgres.intranet.com',
                     'id': 1,
                     'name': 'PostgresSQL',
                     'port': 321}},
      ...
    ]