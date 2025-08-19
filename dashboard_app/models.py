from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EconomicIndicator(models.Model):
    INDICATOR_CHOICES = [
        ('NY.GDP.MKTP.CD', 'GDP (current US$)'),
        ('SP.POP.TOTL', 'Population, total'),
        ('NY.GDP.PCAP.CD', 'GDP per capita (current US$)'),
        ('FP.CPI.TOTL.ZG', 'Inflation, consumer prices (annual %)'),
    ]
    
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    indicator_code = models.CharField(max_length=20, choices=INDICATOR_CHOICES)
    year = models.IntegerField()
    value = models.FloatField()

    class Meta:
        unique_together = ('country', 'indicator_code', 'year')

    def __str__(self):
        return f"{self.country} - {self.get_indicator_code_display()} ({self.year})"