from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    phone = models.CharField(max_length=9, unique=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"


class Car(models.Model):
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=40)
    production_date = models.DateField()
    owner = models.ForeignKey("Owner", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.brand} {self.model}"
