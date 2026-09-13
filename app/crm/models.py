from django.db import models
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название компании")
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company",
        verbose_name="Владелец"
    )

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name

class Storage(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название склада")
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="storages",
        verbose_name="Компания"
    )

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return f"{self.name} ({self.company.name})"

