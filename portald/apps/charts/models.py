from django.db import models


class Chart(models.Model):
    uid = models.CharField(max_length=14)
    caption_text = models.CharField(max_length=50, null=True, blank=True)

    yAxis_plot_value = models.CharField(max_length=30, null=True, blank=True)
    yAxis_plot_type = models.CharField(max_length=30, null=True, blank=True)
    yAxis_title = models.CharField(max_length=40)
    yAxis_format_prefix = models.CharField(max_length=40, null=True, blank=True)

    max_height = models.IntegerField(default=450, blank=True)
    max_width = models.IntegerField(default=700, null=True)

    schema = models.TextField(blank=True, null=True)
    columns = models.CharField(max_length=20, default='col-md-6', blank=True, null=True)

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
        return f'<Chart: {self.uid}:{self.caption_text}>'


class Data(models.Model):
    index = models.IntegerField()

    value = models.CharField(max_length=30)     # first_value,second_value
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def data(self) -> list:
        return self.value.split(',')
