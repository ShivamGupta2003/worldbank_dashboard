from django.db import models

class Country(models.Model):
    """Represents a single country."""
    code = models.CharField(max_length=3, unique=True, primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name

class EconomicIndicator(models.Model):
    """Stores a single economic data point for a country in a given year."""
    INDICATOR_CHOICES = [
        ('NY.GDP.MKTP.CD', 'GDP (current US$)'),
        ('SP.POP.TOTL', 'Population, total'),
        ('NY.GDP.PCAP.CD', 'GDP per capita (current US$)'),
        ('FP.CPI.TOTL.ZG', 'Inflation, consumer prices (annual %)'),
        ('SL.UEM.TOTL.ZS', 'Unemployment, total (% of total labor force)'),
        ('NE.TRD.GNFS.ZS', 'Trade (% of GDP)'),
    ]
    
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="indicators")
    indicator_code = models.CharField(
        max_length=20, 
        choices=INDICATOR_CHOICES,
        db_index=True
    )
    year = models.PositiveIntegerField(db_index=True)
    value = models.FloatField(null=True)

    class Meta:
        unique_together = ('country', 'indicator_code', 'year')
        ordering = ['country', 'indicator_code', 'year'] 

    def __str__(self):
        return f"{self.country.name} - {self.get_indicator_code_display()} ({self.year})"