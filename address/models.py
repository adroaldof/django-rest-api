from django.db import models


class Address(models.Model):
    address = models.CharField(max_length=255)
    number = models.IntegerField()
    complement = models.CharField(max_length=255, null=True)
    zip_code = models.IntegerField()
    neighborhood = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.zip_code} - {self.address}, {self.number}"
