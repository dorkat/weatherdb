from django.db import models

class greeting(models.Model):
    greet_text = models.CharField(max_length=200)
    def __str__(self):              
        return self.greet_text
