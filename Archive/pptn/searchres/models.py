from django.db import models

class restuarant(models.Model):
    name = models.CharField(max_length = 30)
    location = models.CharField(max_length = 50)
    cuisine = models.CharField(max_length = 30)
    walking_time = models.IntegerField()
    grade = models.IntegerField()
    specialties = models.CharField(max_length = 100)
    review = models.TextField()
    latitude = models.DecimalField(max_digits = 10, decimal_places = 7)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 7)

    class Meta:
        db_table = "restuarant"

    def __str__(self):
        return self.title



# Create your models here.
