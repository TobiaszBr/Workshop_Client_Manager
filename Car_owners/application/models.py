from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Owner(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    phone = PhoneNumberField(blank=True, unique=True)


    def __str__(self):
        return f'{self.name} {self.surname}'


class Car(models.Model):
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    production_date = models.DateField()
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.brand} {self.model}'

    def save(self, *args, **kwargs):
        self.brand = self.brand.title()
        self.model = self.model.title()
        super(Car, self).save(*args, **kwargs)