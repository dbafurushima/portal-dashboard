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
    schema = models.CharField(max_length=255)
    columns = models.CharField(max_length=20, default='col-md-6', blank=True, null=True)

    def __str__(self):
        return f'<Chart: {self.uid}:{self.caption_text}>'


class Data(models.Model):
    pass
