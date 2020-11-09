.. code-block::bash

    mng service create "Protheus - dev" \
        --ip 10.1.0.100 \
        --dns "dev.protheus.intranet.com"\
        --port 443

output::

    >> Successfully created.

    { 'dns': 'dev.protheus.intranet.com',
      'id': 3,
      'name': 'Protheus - dev',
      'port': 443}