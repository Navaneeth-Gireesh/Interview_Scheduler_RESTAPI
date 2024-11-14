from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Availability(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    available_date = models.DateField()
    available_time_from = models.TimeField()
    available_time_to = models.TimeField()

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Availability'
        verbose_name_plural = 'Availabilities'

    def TimeValidation(self):
        if self.available_time_from >= self.available_time_to:
            raise ValidationError("The 'available from time' should be before 'available time to' ")
        
    def save(self, *args, **kwargs):
        self.TimeValidation()
        super().save(*args, **kwargs)