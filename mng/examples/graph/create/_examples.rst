.. code-block:: bash

    mng graph create usage_cpu --title "Usage CPU VM01" --prefix "%/s"

output::

    { 'caption_text': 'capition',
    'cid': None,
    'schema': '[{"name": "Time", "type": "date", '
                '"format": "%Y-%m-%d %H-%M"}, '
                '{"name": "title", "type": '
                '"number"}]',
    'subcaption_text': 'subcaption',
    'uid': '3edc_usage_cpu',
    'yAxis_format_prefix': '%/s',
    'yAxis_plot_type': 'line',
    'yAxis_plot_value': 'description value',
    'yAxis_title': 'Usage CPU VM01'}

.. code-block:: bash

    mng graph create usage_cpu_vm0 \
        --cid 1 --title "usage_cpu_vm0" \
        --caption "CPU Analysis" --subcaption "Usage" \
        --description-value "usage cpu is" --prefix "%/min" \
        --stftime "Y-m-d H:M"

output::

    { 'caption_text': 'CPU Analysis',
    'cid': None,
    'schema': '[{"name": "Time", "type": "date", '
                '"format": "%Y-%m-%d %H:%M"}, '
                '{"name": "title", "type": '
                '"number"}]',
    'subcaption_text': 'Usage',
    'uid': '11c3_usage_cpu_vm0',
    'yAxis_format_prefix': '%/min',
    'yAxis_plot_type': 'line',
    'yAxis_plot_value': 'usage cpu is',
    'yAxis_title': 'usage cpu'}