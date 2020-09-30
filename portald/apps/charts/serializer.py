from .models import Chart, Data
from rest_framework import serializers


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = ['id', 'uid', 'caption_text', 'yAxis_plot_value', 'yAxis_plot_type', 'yAxis_title',
                  'yAxis_format_prefix', 'max_height', 'max_width', 'schema', 'columns']


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['id', 'index', 'value', 'chart']
