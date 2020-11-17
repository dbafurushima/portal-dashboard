from django.db import models
from apps.management.models import Client


class Chart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)

    uid = models.CharField(max_length=20)
    caption = models.CharField(max_length=50, null=True, blank=True)
    subcaption = models.CharField(max_length=50, null=True, blank=True)

    yAxis_plot_value = models.CharField(max_length=30, null=True, blank=True)
    yAxis_plot_type = models.CharField(max_length=30, null=True, blank=True)
    yAxis_title = models.CharField(max_length=40)
    yAxis_format_prefix = models.CharField(max_length=40, null=True, blank=True)

    schema = models.TextField(blank=True, null=True)

    from_zabbix = models.BooleanField(default=False, null=True, blank=False)
    number_data = models.IntegerField(default=100, null=True, blank=True)
    itemid = models.CharField(max_length=10, null=True, blank=True)

    @property
    def yAxis(self) -> str:
        return ("[{"
                "plot: {"
                "value: '%s',"
                "type: '%s'"
                "},"
                "format: {"
                "prefix: '%s'"
                "},"
                "title: '%s'"
                "}]" % (self.yAxis_plot_value, self.yAxis_plot_type,
                        self.yAxis_format_prefix, self.yAxis_title))

    def __str__(self):
        return f'<Chart: {self.uid}:{self.caption}>'


class Data(models.Model):
    index = models.IntegerField()

    value = models.TextField()     # first_value,second_value
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def data(self) -> list:
        return [self.value.split(',')[0], int(self.value.split(',')[1])]
