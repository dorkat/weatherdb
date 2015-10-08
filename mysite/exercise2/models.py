from django.db import models

class Cities(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    country_id = models.CharField(max_length=45)
    temperature = models.CharField(max_length=45, blank=True, null=True)
    humidity = models.CharField(max_length=45, blank=True, null=True)
    clouds = models.CharField(max_length=45, blank=True, null=True)
    wind_speed = models.CharField(max_length=45, blank=True, null=True)
    wind_deg = models.CharField(max_length=45, blank=True, null=True)
    max_temp = models.CharField(max_length=45, blank=True, null=True)
    min_temp = models.CharField(max_length=45, blank=True, null=True)
    pressure = models.CharField(max_length=45, blank=True, null=True)
    data_key = models.CharField(max_length=45, blank=True, null=True)
    last_update = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'cities'
        unique_together = (('city_name', 'country_id'),)


class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(unique=True, max_length=45, blank=True, null=True)
    country_full_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'countries'


class City_Temperature_Table(models.Model):
    city_id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'City_Temperature_Table'