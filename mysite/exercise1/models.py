from django.db import models

class greeting(models.Model):
    greet_text = models.CharField(max_length=200)
    name = models.CharField(max_length=45, blank=True, null=True)
    def __str__(self):              
        return self.greet_text
