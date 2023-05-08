from django.db import models
from phonenumber_field.modelfields import PhoneNumberField # a bit of an overkill to use a 3rd party lib for such trivial field


class Owner(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    phone = PhoneNumberField(blank=True, unique=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Car(models.Model):
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20) # I don't like this limit, I own a Lamborghini Aventador LP 750-4 Superveloce 
    production_date = models.DateField()
    owner = models.ForeignKey("Owner", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} {self.model}"

    def save(self, *args, **kwargs): # since you overwrite default `save` method you could actually significantly change the way it works, like implementing a `last_changed` field and setting it here based on current datetime
        self.brand = self.brand.title()
        self.model = self.model.title()
        super(Car, self).save(*args, **kwargs)
