from .models import Chart, Data
from rest_framework import serializers


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = ['id', 'client', 'uid', 'caption', 'yAxis_plot_value', 'yAxis_plot_type', 'yAxis_title',
                  'yAxis_format_prefix', 'schema', 'subcaption', 'from_zabbix', 'number_data', 'itemid']


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['id', 'index', 'value', 'chart']
